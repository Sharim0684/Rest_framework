from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class ReviewDetailThrottle(UserRateThrottle):
    scope = 'throttling_for_review_detail'

class Reviewlistthrottle(UserRateThrottle):
    scope = 'throttling_for_review_list'