-- =============================================
-- FULL CRICBUZZ SCHEMA - READY FOR YOUR PROJECT
-- =============================================

-- Teams
CREATE TABLE IF NOT EXISTS teams (
    team_id BIGINT PRIMARY KEY,
    team_name TEXT NOT NULL,
    team_short_name TEXT
);

-- Venues
CREATE TABLE IF NOT EXISTS venues (
    venue_id BIGINT PRIMARY KEY,
    venue_name TEXT NOT NULL,
    city TEXT
);

-- Series
CREATE TABLE IF NOT EXISTS series (
    series_id BIGINT PRIMARY KEY,
    series_name TEXT NOT NULL
);

-- Matches
CREATE TABLE IF NOT EXISTS matches (
    match_id BIGINT PRIMARY KEY,
    series_id BIGINT REFERENCES series(series_id) ON DELETE SET NULL,
    match_desc TEXT,
    format TEXT,
    state TEXT,
    status TEXT,
    team1_id BIGINT REFERENCES teams(team_id),
    team2_id BIGINT REFERENCES teams(team_id),
    venue_id BIGINT REFERENCES venues(venue_id)
);

-- Players
CREATE TABLE IF NOT EXISTS players (
    player_id BIGINT PRIMARY KEY,
    player_name TEXT NOT NULL
);

-- Batting Stats (per innings)
CREATE TABLE IF NOT EXISTS batting_stats (
    id SERIAL PRIMARY KEY,
    match_id BIGINT REFERENCES matches(match_id) ON DELETE CASCADE,
    player_id BIGINT REFERENCES players(player_id),
    runs INT,
    balls INT,
    fours INT,
    sixes INT,
    strike_rate FLOAT
);

-- Bowling Stats (per innings)
CREATE TABLE IF NOT EXISTS bowling_stats (
    id SERIAL PRIMARY KEY,
    match_id BIGINT REFERENCES matches(match_id) ON DELETE CASCADE,
    player_id BIGINT REFERENCES players(player_id),
    overs FLOAT,
    runs_given INT,
    wickets INT,
    economy FLOAT
);

-- Add missing columns to players table
ALTER TABLE players ADD COLUMN IF NOT EXISTS country TEXT;
ALTER TABLE players ADD COLUMN IF NOT EXISTS playing_role TEXT;
ALTER TABLE players ADD COLUMN IF NOT EXISTS batting_style TEXT;
ALTER TABLE players ADD COLUMN IF NOT EXISTS bowling_style TEXT;
ALTER TABLE players ADD COLUMN IF NOT EXISTS team_id BIGINT REFERENCES teams(team_id);

-- Add index for faster queries
CREATE INDEX IF NOT EXISTS idx_players_country ON players(country);

-- Optional: Add indexes for faster queries (highly recommended)
CREATE INDEX IF NOT EXISTS idx_batting_match ON batting_stats(match_id);
CREATE INDEX IF NOT EXISTS idx_batting_player ON batting_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_match ON bowling_stats(match_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player ON bowling_stats(player_id);

-- Quick verification queries (run these after inserting data)
SELECT 'teams' AS table_name, COUNT(*) FROM teams UNION ALL
SELECT 'venues', COUNT(*) FROM venues UNION ALL
SELECT 'series', COUNT(*) FROM series UNION ALL
SELECT 'matches', COUNT(*) FROM matches UNION ALL
SELECT 'players', COUNT(*) FROM players UNION ALL
SELECT 'batting_stats', COUNT(*) FROM batting_stats UNION ALL
SELECT 'bowling_stats', COUNT(*) FROM bowling_stats;