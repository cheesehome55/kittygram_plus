import datetime as dt
import webcolors

from rest_framework import serializers

from .models import Cat, Owner, Achievement, AchievementCat, CHOICES


class Hex2NameColor(serializers.Field):


    # Для чтения
    def to_representation(self, value):
        return value
    
    # Для записи
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')    
        return data

class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta():
        model = Cat
        fields = ('id', 'name', 'color')


class CatSerializer(serializers.ModelSerializer):
    #owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(many=True, required=False)
    # Создаем кастомное поле которое будет рассчитываться в get_age
    age = serializers.SerializerMethodField()
    #color = Hex2NameColor()
    # Теперь поле примет только значение, упомянутое в списке CHOICES
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'birth_year', 'owner', 'achievements', 'age', 'color')

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year


    def create(self, valideted_data):
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**valideted_data)
            return cat
        
        # Уберём список достижений из словаря validated_data и сохраним его
        temp_achievements = valideted_data.pop('achievements')
        print(temp_achievements)
        # Создадим нового котика пока без достижений, данных нам достаточно
        instance = Cat.objects.create(**valideted_data)
        print(instance)

        for achievement in temp_achievements:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_achievement, status = Achievement.objects.get_or_create(**achievement)
            #instance.achievements.add(current_achievement)

        # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится   
            AchievementCat.objects.create(achievement=current_achievement, cat=instance) 
            #instance = AchievementCat.objects.create(achievement=current_achievement, cat=cat) 

        #instance.achievements.set(temp_achievements)
        return instance    



class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')




