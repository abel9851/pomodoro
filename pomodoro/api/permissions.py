from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedAndIsObjectOwner(IsAuthenticated):
    """
    user가 해당 object의 유저인지 확인한다.
    주의할 점으로는, APIView를 상정하고 만든 클래스로서,
    has_object_permission을 view안에 직접 정의해야한다.

    정의하지 않을 시, ModelSerializer를 사용하고 있을 경우
    rest_framework/renderers.py 532 line에서 obj에 serializer의
    model 인스턴스를 할당하기 때문에 엉뚱한 obj를 사용하게 될 위험이 있다.

    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
