from fastapi import APIRouter
from pydantic import BaseModel

from mealie.routes._base import BaseAdminController, controller
from mealie.services.user_services.user_service import UserService

router = APIRouter(prefix="/config")


class LockoutConfigSummary(BaseModel):
    max_login_attempts: int
    lockout_time_hours: int
    locked_users: int


@controller(router)
class AdminLockoutConfigController(BaseAdminController):
    @router.get("/lockout", response_model=LockoutConfigSummary)
    def get_lockout_config(self):
        """Summarize the login lockout policy together with the number of currently locked users"""
        locked_users = UserService(self.repos).get_locked_users()

        return LockoutConfigSummary(
            max_login_attempts=self.settings.SECURITY_MAX_LOGIN_ATTEMPTS,
            lockout_time_hours=self.settings.SECURITY_USER_LOCKOUT_TIME,
            locked_users=len(locked_users),
        )
