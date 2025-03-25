# matching/services.py


class MatchingService:
    @staticmethod
    def find_matching_services(seeker_preferences):
        """
        Find matching services based on seeker preferences

        :param seeker_preferences: Dict containing search criteria
        :return: Queryset of matching services
        """
        from services.models import Service

        # Basic matching logic
        queryset = Service.objects.filter(is_active=True)

        if seeker_preferences.get('category'):
            queryset = queryset.filter(category__name=seeker_preferences['category'])

        if seeker_preferences.get('max_price'):
            queryset = queryset.filter(price__lte=seeker_preferences['max_price'])

        if seeker_preferences.get('availability_type'):
            queryset = queryset.filter(availability_type=seeker_preferences['availability_type'])

        return queryset
