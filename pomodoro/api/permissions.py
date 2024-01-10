from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedAndIsObjectOwner(IsAuthenticated):
    """
    user가 해당 object의 유저인지 확인한다.
    주의할 점으로는, APIView를 상정하고 만든 클래스로서,
    has_object_permission을 view안에 직접 정의해야한다.

    정의하지 않을 시, ModelSerializer를 사용하고 있을 경우
    rest_framework/renderers.py 532 line에서 obj에 serializer의
    model 인스턴스를 할당하기 때문에 엉뚱한 obj를 사용하게 될 위험이 있다.

    DRF가 제공하는 browsable api로 api request를 할 경우, has_obj_permission이
    2번 호출되고, 각각의 호출에서 사용되는 obj가 다르다.
    view에서 정의한 model serializer가 있을 경우, 그 serializer의 모델 인스턴스가
    obj에 할당되고 그 obj에 user attr가 없다면 에러가 발생하니까 주의해야한다.

    postman으로 request했을 땐 정상 작동하는 것을 확인했다.

    """

    # 추가로 알게 된 점
    # response를 호출할 때
    # response에서 serializer를 호출할 때
    # serializer에 instance가 있다면
    # 그 instance를 obj에 할당한다.
    # 그리고 그 다음 APIView에 정의한
    # permission class에서 has_object_permission 메소드가 정의되어 있다면
    # 호출한다.
    # 즉, response를 할 때 permission class의 메소드를 호출한다.
    # view 안에서 직접 호출하면 2번이나 permission class를 호출하게 된다.
    #
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
