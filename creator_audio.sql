
CREATE TABLE `creator_audio` (
  `track_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `artist` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration` int(10) UNSIGNED DEFAULT NULL,
  `track_type` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `genres` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `moods` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `instruments` json DEFAULT NULL,
  `publish_time` datetime DEFAULT NULL,
  `viper_id` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `license_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `external_artist_url` varchar(2000) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;