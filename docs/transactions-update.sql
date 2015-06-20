use mcp;
alter table mcp.transactions
add column amount decimal;
alter table mcp.transactions
add column description varchar(100);