"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event


class EventView(ViewSet):
  """Level up events view"""
  
  def retrieve(self, request, pk):
    """Handle GET requests for single event
    
    Returns:
      Response -- JSON serialized event
    """
    try:
      event = Event.objects.get(pk=pk)
      serializer = EventSerializer(event)
      return Response(serializer.data)
    except Event.DoesNotExist as ex:
      return Response({'No event exists with specified ID': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  
  def list(self, request):
    """Handle GET requests to get all events
    
    Returns:
      Response -- JSON serialized list of events
    """
    
    events = Event.objects.all()
    
    event_game = request.query_params.get('game', None)
    if event_game is not None:
      events = events.filter(game=event_game)
    
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
  
class EventSerializer(serializers.ModelSerializer):
  """JSON serializer for events
  """
  class Meta:
    model = Event
    fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
    depth = 2    
