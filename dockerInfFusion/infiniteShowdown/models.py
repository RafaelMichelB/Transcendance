from django.db import models

# Create your models here.

class Move(models.Model) :
    name = models.CharField(max_length=100, primary_key=True)
    power = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=255) #Default value = no accuracy check
    side_effect = models.JSONField()
    priority = models.IntegerField(default=0)

class Movepool(models.Model) :
    moves = models.ManyToManyField(Move, related_name=movepool)

class Stats(models.Model) :
    hp = models.IntegerField(default=1)
    attack = models.IntegerField(default=1)
    defense = models.IntegerField(default=1)
    spattack = models.IntegerField(default=1)
    spdefense = models.IntegerField(default=1)
    speed = models.IntegerField(default=1)
    precision = models.IntegerField(default=100)
    evasion = models.IntegerField(default=100)

class Monster(models.Model) :
    name = models.CharField(max_length=100)
    sprite_path = models.CharField(max_length=100)
    stats = models.OneToOneField(Stats, on_delete=models.CASCADE, related_name="monster")
    Ivs = models.JSONField()
    Evs = models.JSONField()
    Movepool = models.OneToOneField(Movepool, on_delete=models.CASCADE, related_name="monster")

class Team(models.Model) :
    mon1 = models.ForgeingKey(Monster, on_delete=models.CASCADE)
    mon2 = models.ForgeingKey(Monster, on_delete=models.CASCADE)
    mon3 = models.ForgeingKey(Monster, on_delete=models.CASCADE)
    mon4 = models.ForgeingKey(Monster, on_delete=models.CASCADE)
    mon5 = models.ForgeingKey(Monster, on_delete=models.CASCADE)
    mon6 = models.ForgeingKey(Monster, on_delete=models.CASCADE)

class Trainer(models.Model) :
    name = models.CharField(max_length=100)
    team = models.ForgeingKey(Team, on_delete=models.CASCADE)

