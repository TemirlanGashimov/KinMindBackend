from django.contrib.auth.models import User
from rest_framework import serializers
from board_app.models import Board

class BoardMemberSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='profile.fullname')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['title', 'members']

class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['title', 'members']

class BoardDetailSerializer(serializers.ModelSerializer):
    members = BoardMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members']
