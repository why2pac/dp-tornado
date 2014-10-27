#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from engine.model import Model as dpModel


class UserModel(dpModel):
    # Method callable by self.model.foo.bar.user.get_user_by_user_uuid from Controller
    def get_user_by_user_uuid(self, user_uuid):
        return user_uuid