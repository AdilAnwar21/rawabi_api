import os
from sqlalchemy import create_engine
import logging
from app.service.common.auth import token_auth
from flask import current_app, url_for
from app import db
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy.exc import SQLAlchemyError


def prepare_bind_and_session_maker(tenant_name):
    if tenant_name not in current_app.config['SQLALCHEMY_BINDS']:
     
        current_app.config['SQLALCHEMY_BINDS'][tenant_name] = current_app.config[
            'SQLALCHEMY_BASE_DATABASE_URI'].format(tenant_name)
    if tenant_name not in current_app.config['SESSION_MAKERS']:
        engine = db.create_engine(current_app.config['SQLALCHEMY_BINDS'][tenant_name], pool_pre_ping=True)
        session_factory = sessionmaker(expire_on_commit=False, bind=engine)
        current_app.config['SESSION_MAKERS'][tenant_name] = scoped_session(session_factory)
    return current_app.config['SESSION_MAKERS'][tenant_name]


def get_tenant_session(tenant_name=None):
    # if not tenant_name:
    #     current_user = token_auth.current_user()
    #     tenant_name = current_user.tenant_name
    #     print(tenant_name)

    # # We are unable to resolve the tenant still then throw an error.
    # if not tenant_name:
    #     raise RuntimeError('No tenant chosen.')

    session_maker = prepare_bind_and_session_maker(tenant_name)
    session = session_maker()
    return session


@contextmanager
def tenant_session_scope(tenant_name =None,max_retries=3):
    """Provide a transactional scope around a series of operations."""
    # tenant_name = os.environ.get("TENANT_NAME")
    logger = logging.getLogger(__name__)
    
    tenant_name = os.environ.get('TENANT_NAME')
    if not tenant_name:
        raise RuntimeError('Tenant Not Found')
        
    session = get_tenant_session(tenant_name)
    retry_count = 0

    while retry_count < max_retries:
        try:
            yield session
            session.commit()
            break  # Exit the loop if the transaction is successful
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error occurred: {str(e)}")
            session.rollback()

            if "Lock wait timeout exceeded" in str(e):
                print("Deadlock detected. Retrying transaction...")
                logger.warning("Deadlock detected. Retrying transaction...")
                retry_count += 1
                continue  # Retry the transaction
            else:
                raise  # Raise the exception if it's not a deadlock
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")  # Log all other exceptions
            raise
        finally:
            print("entered in finally and session closed")
            session.close()