from app.models import EmployeeRole, RoleActivityPermission, ActivityMaster
from app.service.common.auth import token_auth
# from app.models.agents import Employee
# from app.models.members import Member
# from app.models.roleMaster import RoleMaster
from app.service.common.session_factory import tenant_session_scope
from app.errors.types import UnauthorisedAccessException


# def allowed_users(user_types=[], permissions={}, ):
#     def wrapper(f):

#         def wrapped_function(*args, **kwargs):
#             unauthorised = False
#             current_user = token_auth.current_user()
#             if current_user.user_type not in user_types:
#                 does_not_have_permissions = True
#                 if current_user.user_type != 'tenant_admin':
#                     with tenant_session_scope() as session:
#                         if 'employee' in permissions.keys():
#                             emps = session.query(Member).filter(Member.user_id == current_user.id).join(Employee,Employee.member_id==Member.id).join(EmployeeRole,
#                                                                                                         EmployeeRole.employee_id == Employee.id).join(
#                                 RoleMaster, RoleMaster.id == EmployeeRole.role_id).join(RoleActivityPermission,
#                                                                                     RoleActivityPermission.role_id == EmployeeRole.id,getattr(RoleActivityPermission, permissions['value']) == 'yes').join(ActivityMaster,
#                                                                                                     ActivityMaster.activity ==
#                                                                                                     permissions['value']).all()
#                             for emp in emps:
#                                 if emp.RoleActivityPermission.getattr(RoleActivityPermission, permissions['name']) == "yes":
#                                     does_not_have_permissions = False
#                                     break
#                         elif 'customer' in permissions.keys():
#                             does_not_have_permissions = False
#                 if does_not_have_permissions:
#                     unauthorised = True

#             if unauthorised:
#                 raise UnauthorisedAccessException(message="Un-authorized access exception")

#             return f(*args, **kwargs)

#         # Renaming the function name:
#         wrapped_function.__name__ = f.__name__

#         return wrapped_function

#     return wrapper
