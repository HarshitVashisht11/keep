"""MSSQL

Revision ID: 174e14a72483
Revises:
Create Date: 2024-07-16 16:06:26.927036

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "174e14a72483"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tenant",
        sa.Column("configuration", sa.JSON(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column(
            "username", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=False
        ),
        sa.Column("password_hash", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("role", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("last_sign_in", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "action",
        sa.Column("action_raw", sa.TEXT(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("use", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column(
            "description", sqlmodel.sql.sqltypes.AutoString(length=2048), nullable=True
        ),
        sa.Column(
            "installed_by", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False
        ),
        sa.Column("installation_time", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "name", "use"),
    )
    op.create_table(
        "alert",
        sa.Column("timestamp", mssql.DATETIME2(precision=3), nullable=False),
        sa.Column("event", sa.JSON(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("provider_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("provider_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "fingerprint", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=False
        ),
        sa.Column("alert_hash", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_alert_fingerprint"), "alert", ["fingerprint"], unique=False
    )
    op.create_index(op.f("ix_alert_timestamp"), "alert", ["timestamp"], unique=False)
    op.create_table(
        "alertaudit",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column("fingerprint", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("tenant_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("action", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_alert_audit_fingerprint", "alertaudit", ["fingerprint"], unique=False
    )
    op.create_index(
        "ix_alert_audit_tenant_id", "alertaudit", ["tenant_id"], unique=False
    )
    op.create_index(
        "ix_alert_audit_tenant_id_fingerprint",
        "alertaudit",
        ["tenant_id", "fingerprint"],
        unique=False,
    )
    op.create_index(
        "ix_alert_audit_timestamp", "alertaudit", ["timestamp"], unique=False
    )
    op.create_table(
        "alertdeduplicationfilter",
        sa.Column("fields", sa.JSON(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column(
            "matcher_cel", sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "alertenrichment",
        sa.Column("enrichments", sa.JSON(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column(
            "alert_fingerprint",
            sqlmodel.sql.sqltypes.AutoString(length=256),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("alert_fingerprint"),
    )
    op.create_table(
        "alertraw",
        sa.Column("raw_alert", sa.JSON(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dashboard",
        sa.Column(
            "dashboard_config", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column(
            "dashboard_name",
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=False,
        ),
        sa.Column(
            "created_by", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "updated_by", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_private", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id", "dashboard_name", name="unique_dashboard_name_per_tenant"
        ),
    )
    op.create_index(
        op.f("ix_dashboard_dashboard_name"),
        "dashboard",
        ["dashboard_name"],
        unique=False,
    )
    op.create_table(
        "extractionrule",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column(
            "description", sqlmodel.sql.sqltypes.AutoString(length=2048), nullable=True
        ),
        sa.Column(
            "created_by", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "updated_by", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("pre", sa.Boolean(), nullable=False),
        sa.Column(
            "condition", sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=True
        ),
        sa.Column(
            "attribute", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False
        ),
        sa.Column(
            "regex", sqlmodel.sql.sqltypes.AutoString(length=1024), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "mappingrule",
        sa.Column("matchers", sa.JSON(), nullable=True),
        sa.Column("rows", sa.JSON(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column(
            "description", sqlmodel.sql.sqltypes.AutoString(length=2048), nullable=True
        ),
        sa.Column(
            "file_name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column(
            "created_by", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("override", sa.Boolean(), nullable=False),
        sa.Column(
            "condition", sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=True
        ),
        sa.Column(
            "updated_by", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column("last_updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "preset",
        sa.Column("options", sa.JSON(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=False),
        sa.Column(
            "created_by", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False
        ),
        sa.Column("is_private", sa.Boolean(), nullable=True),
        sa.Column("is_noisy", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("tenant_id", "name"),
    )
    op.create_index(
        op.f("ix_preset_created_by"), "preset", ["created_by"], unique=False
    )
    op.create_index(op.f("ix_preset_tenant_id"), "preset", ["tenant_id"], unique=False)
    op.create_table(
        "provider",
        sa.Column("validatedScopes", sa.JSON(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column(
            "installed_by", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False
        ),
        sa.Column("installation_time", sa.DateTime(), nullable=False),
        sa.Column(
            "configuration_key",
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=False,
        ),
        sa.Column("consumer", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "name"),
    )
    op.create_table(
        "rule",
        sa.Column("definition", sa.JSON(), nullable=True),
        sa.Column("grouping_criteria", sa.JSON(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("definition_cel", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("timeframe", sa.Integer(), nullable=False),
        sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("creation_time", sa.DateTime(), nullable=False),
        sa.Column("updated_by", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("update_time", sa.DateTime(), nullable=True),
        sa.Column(
            "group_description", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column(
            "item_description", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tenantapikey",
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("reference_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "key_hash", sqlmodel.sql.sqltypes.AutoString(length=64), nullable=False
        ),
        sa.Column("is_system", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column(
            "system_description", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("role", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_used", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("key_hash"),
    )
    op.create_table(
        "workflow",
        sa.Column("workflow_raw", sa.TEXT(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column(
            "name", sqlmodel.sql.sqltypes.AutoString(length=1024), nullable=False
        ),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "created_by", sqlmodel.sql.sqltypes.AutoString(length=1024), nullable=False
        ),
        sa.Column("updated_by", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("creation_time", sa.DateTime(), nullable=False),
        sa.Column("interval", sa.Integer(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "group",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column(
            "rule_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("creation_time", sa.DateTime(), nullable=False),
        sa.Column(
            "group_fingerprint", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["rule_id"],
            ["rule.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "workflowexecution",
        sa.Column("results", sa.JSON(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False),
        sa.Column(
            "workflow_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("started", sa.DateTime(), nullable=False),
        sa.Column(
            "triggered_by",
            sqlmodel.sql.sqltypes.AutoString(length=1024),
            nullable=False,
        ),
        sa.Column(
            "status", sqlmodel.sql.sqltypes.AutoString(length=1024), nullable=False
        ),
        sa.Column("is_running", sa.Integer(), nullable=False),
        sa.Column("timeslot", sa.Integer(), nullable=False),
        sa.Column("execution_number", sa.Integer(), nullable=False),
        sa.Column(
            "error", sqlmodel.sql.sqltypes.AutoString(length=8000), nullable=True
        ),
        sa.Column("execution_time", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflow.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workflow_id", "execution_number", "is_running", "timeslot"
        ),
    )
    op.create_table(
        "alerttogroup",
        sa.Column(
            "tenant_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column(
            "alert_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.Column(
            "group_id", sqlmodel.sql.sqltypes.AutoString(length=36), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["alert_id"],
            ["alert.id"],
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["group.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("alert_id", "group_id"),
    )
    op.create_table(
        "workflowexecutionlog",
        sa.Column("context", sa.JSON(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "workflow_execution_id",
            sqlmodel.sql.sqltypes.AutoString(length=36),
            nullable=False,
        ),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("message", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["workflow_execution_id"],
            ["workflowexecution.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "workflowtoalertexecution",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "workflow_execution_id",
            sqlmodel.sql.sqltypes.AutoString(length=36),
            nullable=False,
        ),
        sa.Column(
            "alert_fingerprint",
            sqlmodel.sql.sqltypes.AutoString(length=256),
            nullable=False,
        ),
        sa.Column(
            "event_id", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["workflow_execution_id"],
            ["workflowexecution.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("workflow_execution_id", "alert_fingerprint"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("workflowtoalertexecution")
    op.drop_table("workflowexecutionlog")
    op.drop_table("alerttogroup")
    op.drop_table("workflowexecution")
    op.drop_table("group")
    op.drop_table("workflow")
    op.drop_table("tenantapikey")
    op.drop_table("rule")
    op.drop_table("provider")
    op.drop_index(op.f("ix_preset_tenant_id"), table_name="preset")
    op.drop_index(op.f("ix_preset_created_by"), table_name="preset")
    op.drop_table("preset")
    op.drop_table("mappingrule")
    op.drop_table("extractionrule")
    op.drop_index(op.f("ix_dashboard_dashboard_name"), table_name="dashboard")
    op.drop_table("dashboard")
    op.drop_table("alertraw")
    op.drop_table("alertenrichment")
    op.drop_table("alertdeduplicationfilter")
    op.drop_index("ix_alert_audit_timestamp", table_name="alertaudit")
    op.drop_index("ix_alert_audit_tenant_id_fingerprint", table_name="alertaudit")
    op.drop_index("ix_alert_audit_tenant_id", table_name="alertaudit")
    op.drop_index("ix_alert_audit_fingerprint", table_name="alertaudit")
    op.drop_table("alertaudit")
    op.drop_index(op.f("ix_alert_timestamp"), table_name="alert")
    op.drop_index(op.f("ix_alert_fingerprint"), table_name="alert")
    op.drop_table("alert")
    op.drop_table("action")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table("user")
    op.drop_table("tenant")
    # ### end Alembic commands ###
