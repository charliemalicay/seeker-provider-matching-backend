# matching/utils.py


def calculate_match_score(seeker, service_provider):
    """
    Calculate match compatibility score between seeker and provider

    :param seeker: User object (seeker)
    :param service_provider: User object (provider)
    :return: Compatibility score (0-100)
    """
    score = 50  # Base score

    # Location proximity (simple example)
    if seeker.location and service_provider.location:
        # You would replace this with a more sophisticated location matching
        if seeker.location == service_provider.location:
            score += 25

    # Service history and reviews could be added here in future iterations

    return min(score, 100)
