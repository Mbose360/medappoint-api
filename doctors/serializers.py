from rest_framework import serializers
from models import Schedule

from rest_framework import serializers

from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = [
            "id",
            "doctor",
            "day_of_week",
            "start_time",
            "end_time",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        start = data.get("start_time")
        end = data.get("end_time")

        # 1. Make sure the schedule has a valid time range
        if start >= end:
            raise serializers.ValidationError(
                "Start time must be before end time."
            )

        # 2. Check whether the exact same schedule already exists
        exist = Schedule.objects.filter(
            doctor=data["doctor"],
            day_of_week=data["day_of_week"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        ).exists()

        if exist:
            raise serializers.ValidationError(
                "This schedule already exists."
            )

        # 3. Get schedules for the same doctor on the same day
        compares = Schedule.objects.filter(
            doctor=data["doctor"],
            day_of_week=data["day_of_week"],
        )

        # 4. Check for overlapping schedules
        for compare in compares:
            if (
                compare.start_time < end
                and start < compare.end_time
            ):
                raise serializers.ValidationError(
                    "There is an overlap with an existing schedule."
                )

        return data