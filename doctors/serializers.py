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
        read_only_fields = ["id", "doctor"]

    def validate(self, data):
        start = data.get("start_time")
        end = data.get("end_time")

        # 1. Start time must be before end time
        if start >= end:
            raise serializers.ValidationError(
                "Start time must be before end time."
            )

        # 2. Get the doctor from the serializer context
        doctor = self.context["doctor"]

        # 3. Check for an exact duplicate
        exist = Schedule.objects.filter(
            doctor=doctor,
            day_of_week=data["day_of_week"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        ).exists()

        if exist:
            raise serializers.ValidationError(
                "This schedule already exists."
            )

        # 4. Check for overlapping schedules
        compares = Schedule.objects.filter(
            doctor=doctor,
            day_of_week=data["day_of_week"],
        )

        for compare in compares:
            if (
                compare.start_time < end
                and start < compare.end_time
            ):
                raise serializers.ValidationError(
                    "There is an overlap with an existing schedule."
                )

        return data