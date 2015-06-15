delete from mcp.members;
delete from mcp.wallets;

insert into mcp.wallets (name, balance)
values
('pop', 100), -- $1.00
('pop', 50), -- $0.50
('pop', 0); -- $0.00 (unused/unassigned)

insert into mcp.members (first_name, last_name, twitter_name, nickname, irc_name, email, fob_field, password, last_unlock, announce, wallet_id)
values
('Travis', 'Ralston', 'turt2live', 'turt2live', 'turt2live', 'travis.ralston@test.com', '5960989', 'notreal', current_timestamp(), 0, (select id from mcp.wallets where balance = 100 limit 1)),
('Test', 'User1', 'TestUser1', 'TestUser1', 'TestUser1', 'test.user1@test.com', '5977385', 'notreal', current_timestamp(), 0, (select id from mcp.wallets where balance = 50 limit 1)),
('Test', 'User2', 'TestUser2', 'TestUser2', 'TestUser2', 'test.user2@test.com', '5951457', 'notreal', current_timestamp(), 0, null); -- Intentionally don't use the third wallet created

select nickname, fob_field, balance
from mcp.members
join mcp.wallets
on members.wallet_id = wallets.id;

-- select * from mcp.members;
-- select * from mcp.wallets;
