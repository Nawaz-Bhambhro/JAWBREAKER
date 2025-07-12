from rest_framework import serializers
from .models import CommunicationThread, Message, MessageTemplate, MessageReadStatus
from patients.serializers import PatientBasicSerializer
from authentication.serializers import UserBasicSerializer


class MessageTemplateSerializer(serializers.ModelSerializer):
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    
    class Meta:
        model = MessageTemplate
        fields = '__all__'


class MessageReadStatusSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = MessageReadStatus
        fields = ['user', 'read_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserBasicSerializer(read_only=True)
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    read_status = MessageReadStatusSerializer(source='messagereadstatus_set', many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['sender', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class CommunicationThreadSerializer(serializers.ModelSerializer):
    patient = PatientBasicSerializer(read_only=True)
    created_by = UserBasicSerializer(read_only=True)
    participants = UserBasicSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CommunicationThread
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return {
                'id': last_message.id,
                'sender': last_message.sender.full_name,
                'content': last_message.content[:100] + '...' if len(last_message.content) > 100 else last_message.content,
                'created_at': last_message.created_at,
                'message_type': last_message.get_message_type_display()
            }
        return None
    
    def get_unread_count(self, obj):
        user = self.context.get('request').user
        if user:
            return obj.messages.exclude(read_by=user).count()
        return 0


class CommunicationThreadDetailSerializer(serializers.ModelSerializer):
    patient = PatientBasicSerializer(read_only=True)
    created_by = UserBasicSerializer(read_only=True)
    participants = UserBasicSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = CommunicationThread
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CommunicationThreadCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = CommunicationThread
        exclude = ['created_by', 'participants', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        validated_data['created_by'] = self.context['request'].user
        
        thread = super().create(validated_data)
        
        # Add participants
        if participant_ids:
            thread.participants.set(participant_ids)
        
        # Always add the creator as a participant
        thread.participants.add(self.context['request'].user)
        
        return thread


class AIMessageGenerationSerializer(serializers.Serializer):
    """Serializer for AI message generation requests"""
    template_id = serializers.IntegerField(required=False)
    message_type = serializers.CharField()
    context_data = serializers.JSONField(required=False)
    custom_prompt = serializers.CharField(required=False)


class CommunicationStatsSerializer(serializers.Serializer):
    """Serializer for communication statistics"""
    total_threads = serializers.IntegerField()
    active_threads = serializers.IntegerField()
    urgent_threads = serializers.IntegerField()
    unread_messages = serializers.IntegerField()
    avg_response_time = serializers.CharField()
    messages_by_type = serializers.JSONField()
    top_participants = serializers.JSONField()
