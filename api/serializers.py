from rest_framework import serializers

class ManualInputSerializer(serializers.Serializer):
    Flow_Duration = serializers.FloatField()
    Flow_Byts_s = serializers.FloatField()
    Tot_Fwd_Pkts = serializers.FloatField()
    Tot_Bwd_Pkts = serializers.FloatField()
    Fwd_Pkt_Len_Max = serializers.FloatField()
    Bwd_Pkt_Len_Max = serializers.FloatField()
    Fwd_IAT_Mean = serializers.FloatField()
    Bwd_IAT_Mean = serializers.FloatField()
    SYN_Flag_Cnt = serializers.FloatField()
    RST_Flag_Cnt = serializers.FloatField()
    ACK_Flag_Cnt = serializers.FloatField()
    Flow_Pkts_s = serializers.FloatField()
