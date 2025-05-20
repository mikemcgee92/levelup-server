"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer


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
  
  def create(self, request):
    """Handles POST operations
    
    Returns
      Response -- JSON serialized event instance
    """
    organizer = Gamer.objects.get(uid=request.data["organizer"])
    game = Game.objects.get(pk=request.data["game"])
    
    event = Event.objects.create(
      game = game,
      description = request.data["description"],
      date = request.data["date"],
      time = request.data["time"],
      organizer = organizer,
    )
    serializer = EventSerializer(event)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for an event
    
    Returns:
      Response -- Empty body with 204 status code
    """
    
    event = Event.objects.get(pk=pk)
    event.description = request.data["description"]
    event.date = request.data["date"]
    event.time = request.data["time"]
    
    event_game = Game.objects.get(pk=request.data["game"])
    event.game = event_game
    event_organizer = Gamer.objects.get(uid=request.data["organizer"])
    event.organizer = event_organizer
    event.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
  
class EventSerializer(serializers.ModelSerializer):
  """JSON serializer for events
  """
  class Meta:
    model = Event
    fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
    depth = 2    
