from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd
from .predictor import predict_dos_from_csv, predict_dos_from_input
from django.core.files import File
# Feature columns as in your HTML form (original names)
feature_columns = [
    'Flow Duration', 'Flow_Byts/s', 'Tot_Fwd_Pkts', 'Tot_Bwd_Pkts', 
    'Fwd_Pkt_Len_Max', 'Bwd_Pkt_Len_Max', 'Fwd_IAT_Mean', 'Bwd_IAT_Mean',
    'SYN_Flag_Cnt', 'RST_Flag_Cnt', 'ACK_Flag_Cnt', 'Flow_Pkts/s'
]

from django.conf import settings

from .models import Upload  # your Upload model
import uuid
import json

def upload_and_predict(request):
    context = {'manual_input_fields': feature_columns}

    rename_map = {
        'Flow Duration': 'Flow_Duration',
        'Flow_Byts/s': 'Flow_Byts_s',
        'Flow_Pkts/s': 'Flow_Pkts_s'
    }

    if request.method == 'POST':
        # --- CSV Upload Form ---
        if 'predict_csv' in request.POST:
            if 'csv_file' in request.FILES:
                csv_file = request.FILES['csv_file']
                context['csv_ready'] = True

                upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
                os.makedirs(upload_dir, exist_ok=True)

                unique_filename = f"{uuid.uuid4()}_{csv_file.name}"
                fs = FileSystemStorage(location=upload_dir)
                filename = fs.save(unique_filename, csv_file)
                file_path = fs.path(filename)

                try:
                    results_df = predict_dos_from_csv(file_path)

                    output_dir = os.path.join(settings.MEDIA_ROOT, 'predictions')
                    os.makedirs(output_dir, exist_ok=True)
                    output_filename = f"prediction_{uuid.uuid4()}.csv"
                    output_path = os.path.join(output_dir, output_filename)
                    results_df.to_csv(output_path, index=False)

                    context['download_link'] = os.path.join(settings.MEDIA_URL, 'predictions', output_filename)

                    label_counts = results_df['Predicted_Label'].value_counts().to_dict()
                    context['normal_count'] = label_counts.get('Normal', 0)
                    context['dos_count'] = label_counts.get('DoS Attack', label_counts.get('DOS', 0))

                    if request.user.is_authenticated:
                        upload_entry = Upload.objects.create(
                            user=request.user,
                            csv_file=os.path.join('uploads', unique_filename),
                            original_filename=csv_file.name,
                            dos_count=context['dos_count'],
                            normal_count=context['normal_count'],
                        )
                        # Save output file to upload_entry
                        with open(output_path, 'rb') as f:
                            upload_entry.output_file.save(output_filename, File(f), save=True)

                except Exception as e:
                    context['error'] = f"Error processing CSV file: {str(e)}"
            else:
                context['error'] = "No CSV file provided."

        # --- Manual Input Form ---
        elif 'predict_manual' in request.POST:
            try:
                manual_input_dict = {}
                for field in feature_columns:
                    val = request.POST.get(field, "").strip()
                    if val.lower() == 'false':
                        val = 0.0
                    elif val.lower() == 'true':
                        val = 1.0
                    else:
                        val = val.replace(',', '')
                        val = float(val)

                    renamed_key = rename_map.get(field, field)
                    manual_input_dict[renamed_key] = val

                model_feature_columns = [
                    'Flow_Duration', 'Flow_Byts_s', 'Tot_Fwd_Pkts', 'Tot_Bwd_Pkts',
                    'Fwd_Pkt_Len_Max', 'Bwd_Pkt_Len_Max', 'Fwd_IAT_Mean', 'Bwd_IAT_Mean',
                    'SYN_Flag_Cnt', 'RST_Flag_Cnt', 'ACK_Flag_Cnt', 'Flow_Pkts_s'
                ]

                manual_input = [manual_input_dict[col] for col in model_feature_columns]
                prediction_result = predict_dos_from_input(manual_input)
                context['manual_prediction'] = prediction_result.get('Prediction', 'Unknown')
            except Exception as e:
                context['error'] = f"Invalid manual input: {str(e)}"

    # Load upload history
    if request.user.is_authenticated:
        user_uploads = Upload.objects.filter(user=request.user).order_by('-uploaded_at')
        context['user_uploads'] = user_uploads

    return render(request, 'dos_detection_app/upload_predict.html', context)

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import re
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        # Check if username exists
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        # Check if email exists
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
        # Password strength validation
        elif len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        elif not re.search(r"[A-Z]", password1):
            messages.error(request, "Password must contain at least one uppercase letter.")
        elif not re.search(r"[a-z]", password1):
            messages.error(request, "Password must contain at least one lowercase letter.")
        elif not re.search(r"[0-9]", password1):
            messages.error(request, "Password must contain at least one digit.")
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password1):
            messages.error(request, "Password must contain at least one special character.")
        else:
            # All validations passed — create user
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Account created successfully.")
            return redirect('login')

    return render(request, 'dos_detection_app/signup.html')


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
@login_required
def upload_history(request):
    uploads = Upload.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'dos_detection_app/history.html', {'uploads': uploads})

def user_logout(request):
    logout(request)
    return redirect('login')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')  # Redirect to Django Admin
            return redirect('upload_and_predict')  # Regular user dashboard
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'dos_detection_app/login.html')

@login_required
def upload_history(request):
    user_uploads = Upload.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'dos_detection_app/history.html', {'user_uploads': user_uploads})