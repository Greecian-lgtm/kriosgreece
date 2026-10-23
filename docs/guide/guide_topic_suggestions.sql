-- KRIOS Page Guide: opt-in topic suggestions (Phase 2a). NOT APPLIED. Director chooses the Supabase project first.
-- Visitors can insert only; nobody can read through the public API. No IP, no user agent, no identifiers stored.
create table if not exists public.guide_topic_suggestions (
  id bigint generated always as identity primary key,
  question text not null check (char_length(question) between 3 and 300),
  lang text not null check (lang in ('en','el','es')),
  day date not null default current_date,
  created_at timestamptz not null default now()
);
alter table public.guide_topic_suggestions enable row level security;
revoke all on public.guide_topic_suggestions from anon, authenticated;
grant insert (question, lang, day) on public.guide_topic_suggestions to anon;
create policy "visitors may suggest" on public.guide_topic_suggestions for insert to anon with check (true);
-- Scrub e-mail addresses and phone numbers server-side as well (the page already scrubs them).
create or replace function public.guide_scrub() returns trigger language plpgsql as $$
begin
  new.question := regexp_replace(new.question, '[[:alnum:]._%+-]+@[[:alnum:].-]+\.[[:alpha:]]{2,}', '[email removed]', 'g');
  new.question := regexp_replace(new.question, '\+?[0-9][0-9 ().-]{7,}[0-9]', '[number removed]', 'g');
  new.day := current_date;
  return new;
end $$;
drop trigger if exists guide_scrub_t on public.guide_topic_suggestions;
create trigger guide_scrub_t before insert on public.guide_topic_suggestions for each row execute function public.guide_scrub();
-- Rate limiting: put a small Edge Function in front (per-IP counter held in memory only, never written to this table),
-- or use the Supabase API gateway limits. The page posts to data/guide_config.json "suggest_url".
