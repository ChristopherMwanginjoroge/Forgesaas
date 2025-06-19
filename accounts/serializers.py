from rest_framework import serializers


class OtpVerificationSerializer(serializers.Serializer):
    otp_code=serializers.CharField(max_length=6)
    otp_token=serializers.CharField(max_length=64)

    def validate_otp_code(self,value):
        if not value.is_didgit() or len(value) !=6:
            raise serializers.ValidationError("invalid otp code format")
        return value
    
    def validate_otp_token(self,value):
        if len(value)< 20 or len(value) > 64:
            raise serializers.ValidationError("Invalid format for otp token")
        
        valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")

        if not all(c in valid_chars for c in value):
            raise serializers.ValidationError("Otp token contains invalid characters")
        
        return value
    
class OtpResendSerializer(serializers.Serializer):
    email=serializers.EmailField()

    