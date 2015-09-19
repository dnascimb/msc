drop table if exists service_requests;
create table service_requests (
  id text primary key,
  'number' integer not null,
  'type' integer not null,
  'status' text not null,
  'updated_at' text not null,
  'provider' text not null
 );
 drop table if exists user_profiles;
 create table user_profiles (
  id text primary key,
  'user_name' text not null,
  'user_company' text not null,
  'email' text not null,
  'phone' text not null,
  'address1' text not null,
  'address2' text not null,
  'city' text not null,
  'state' text not null,
  'zip' text not null,
  'country' text not null,
  'updated_at' text not null
);
