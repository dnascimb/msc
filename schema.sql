drop table if exists service_requests;
create table service_requests (
  id text primary key autoincrement,
  'number' integer not null,
  'type' integer not null,
  'status' text not null,
  'updated_at' text not null,
  'provider' text not null
);
