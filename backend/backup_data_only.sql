--
-- PostgreSQL database dump
--

\restrict 7E0g42tT5CrlvGhop0PHhwkoAeo6zcjdEFRbWfgnyHgVv1uRtnZVJwzJh0h06EV

-- Dumped from database version 14.23 (Ubuntu 14.23-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.23 (Ubuntu 14.23-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (294, 'pbkdf2_sha256$720000$a0eWRGZPfCoG9yoyE23ySX$r0FuAEsL4y0XL0pswpd4AqWLNJ2QGP8M3/vHCGnPhuA=', NULL, false, 'test_user_1', 'test_user_1@example.com', 'Danielle', 'Johnson', '', '', '', NULL, 'user', '2025-11-05 10:50:40.480531+00', '2026-06-16 19:04:02.507365+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (295, 'pbkdf2_sha256$720000$xGqlbMtIppF0Iq7nQvCDoJ$h2N3Ew7LK4f0XPtONRWk03Z9ErJV5sucOeAQFmHIDqA=', NULL, false, 'test_user_2', 'test_user_2@example.com', 'Joshua', 'Walker', '', '', '', NULL, 'user', '2024-09-21 06:25:35.480531+00', '2026-06-16 19:04:02.507455+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (296, 'pbkdf2_sha256$720000$jL07aPCE1TA05d80wdZX5e$Gw6yRd911QU/pUlx15o+R7/+Q4LDvSZAomDZkHyPNJI=', NULL, false, 'test_user_3', 'test_user_3@example.com', 'Jill', 'Rhodes', '', '', '', NULL, 'user', '2024-07-16 05:17:57.480531+00', '2026-06-16 19:04:02.507538+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (297, 'pbkdf2_sha256$720000$YR1swrKjm51HpnLyaw9tu0$vgcFF+49ydOUDJIb1ig1cApSHiPDQFts2+7E6oM4IeY=', NULL, false, 'test_user_4', 'test_user_4@example.com', 'Patricia', 'Miller', '', '', '', NULL, 'user', '2026-01-23 18:34:05.480531+00', '2026-06-16 19:04:02.50762+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (298, 'pbkdf2_sha256$720000$aBwULLOwbvsuOmQMikajzA$TgndpHEvUT2GWWrZz490YpTtU8k2e2vkaOKzgmmIZP4=', NULL, false, 'test_user_5', 'test_user_5@example.com', 'Robert', 'Johnson', '', '', '', NULL, 'user', '2025-01-26 09:58:59.480531+00', '2026-06-16 19:04:02.507705+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (299, 'pbkdf2_sha256$720000$DDR07sD4qHcVfKabfHreQz$8BJrZNbuArOz7CgDySR7glKc/lxeXpfhsAAn9lpYl5Y=', NULL, false, 'test_user_6', 'test_user_6@example.com', 'Jeffery', 'Wagner', '', '', '', NULL, 'user', '2025-01-03 00:10:48.480531+00', '2026-06-16 19:04:02.507788+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (300, 'pbkdf2_sha256$720000$pnfi4y5lBD8GFlHUDRFvt8$NibXc3RtOnN18ElkAZPUPWr9uQNc8iF4zuRC4wHNHEQ=', NULL, false, 'test_user_7', 'test_user_7@example.com', 'Anthony', 'Gonzalez', '', '', '', NULL, 'user', '2024-12-17 04:00:53.480531+00', '2026-06-16 19:04:02.507869+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (301, 'pbkdf2_sha256$720000$4Hs0N2NB2vvSdh95fWIufC$UMleWvnXmbvjDjWuSeLnHH9uw7DqAt5vX62wbfpzMxY=', NULL, false, 'test_user_8', 'test_user_8@example.com', 'Debra', 'Gardner', '', '', '', NULL, 'user', '2024-10-13 04:14:25.480531+00', '2026-06-16 19:04:02.50795+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (302, 'pbkdf2_sha256$720000$PyUPbGvUyvZUPIxO9s4Vg3$uBwJknDGlBUuLqZcQuKhEl7BhsqZPq7LNLyuIy9+5yI=', NULL, false, 'test_user_9', 'test_user_9@example.com', 'Jeffrey', 'Lawrence', '', '', '', NULL, 'user', '2026-01-19 19:53:00.480531+00', '2026-06-16 19:04:02.508061+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (303, 'pbkdf2_sha256$720000$5rzaxWRI8oXg1bg9ZLFcfK$XaEnqrCsLfvgFha6RdD6tNsgtCXJlBycqObe8sI2Wlw=', NULL, false, 'test_user_10', 'test_user_10@example.com', 'Lisa', 'Smith', '', '', '', NULL, 'user', '2024-09-14 09:42:48.480531+00', '2026-06-16 19:04:02.508144+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (304, 'pbkdf2_sha256$720000$yy8Am1KkfbJ4VisIT0ke8d$UlhG9QmiShGdAGX0XfTZKiHUqMJ3qXoSWpe9ZMOlwXw=', NULL, false, 'test_user_11', 'test_user_11@example.com', 'Linda', 'Wolfe', '', '', '', NULL, 'user', '2025-12-04 09:39:27.480531+00', '2026-06-16 19:04:02.508242+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (305, 'pbkdf2_sha256$720000$bqgpr0VKSgpXRX1twE8Uwx$RVOQLY65P4Gn0Zvj20cOueeDoCTeUx1MzU0nXjGtA/E=', NULL, false, 'test_user_12', 'test_user_12@example.com', 'Matthew', 'Moore', '', '', '', NULL, 'user', '2026-01-23 02:06:44.480531+00', '2026-06-16 19:04:02.508322+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (306, 'pbkdf2_sha256$720000$PioSjq3RgnhgcRKOrHj2MG$fpMhQk9sSL02bz/U9WNUgWSqkom7o2QtQh8JKMlcYDg=', NULL, false, 'test_user_13', 'test_user_13@example.com', 'Susan', 'Rogers', '', '', '', NULL, 'user', '2026-05-20 18:29:51.480531+00', '2026-06-16 19:04:02.508402+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (307, 'pbkdf2_sha256$720000$InPZqG8Cg4J9cSWgFrlZXK$lycaTizyZmF3zsv0cRARRrhq/Ki2QV/VtLw83OGcjcQ=', NULL, false, 'test_user_14', 'test_user_14@example.com', 'Christopher', 'Davis', '', '', '', NULL, 'user', '2025-08-24 09:26:02.480531+00', '2026-06-16 19:04:02.508482+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (308, 'pbkdf2_sha256$720000$5nhuqe0pocMgRxGu6T0VPp$fYB3YA4SKm1v8rCBdio+CpivDUAtz714id/dB1W+m2M=', NULL, false, 'test_user_15', 'test_user_15@example.com', 'Melanie', 'Munoz', '', '', '', NULL, 'user', '2024-09-02 07:43:20.480531+00', '2026-06-16 19:04:02.508561+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (309, 'pbkdf2_sha256$720000$Ep6QiLo9Ql2goMw40cpAmg$AG0A4D/Th01p2Cr6L+4/B7KG7+0T22i/dIg1C7YK5g4=', NULL, false, 'test_user_16', 'test_user_16@example.com', 'Lindsay', 'Blair', '', '', '', NULL, 'user', '2025-09-28 10:38:35.480531+00', '2026-06-16 19:04:02.50864+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (310, 'pbkdf2_sha256$720000$Ycnx7CRs6BNutQ6tYLxW7r$gJPgrzESBgIXFTQmzYLzvELDz3yeni6A/Dh3gjfl/hU=', NULL, false, 'test_user_17', 'test_user_17@example.com', 'Amanda', 'Dudley', '', '', '', NULL, 'user', '2025-05-20 12:15:28.480531+00', '2026-06-16 19:04:02.508723+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (311, 'pbkdf2_sha256$720000$z9ArdOfvEHLG65SycH953V$a0nMEpdZ5Dji6ddZkyb/0tro9leN1QyJz4nvNpkX9ss=', NULL, false, 'test_user_18', 'test_user_18@example.com', 'Nicholas', 'Arnold', '', '', '', NULL, 'user', '2024-07-21 11:32:13.480531+00', '2026-06-16 19:04:02.508805+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (312, 'pbkdf2_sha256$720000$AlTGR8DsGXhoa9HpQ8kQws$QUUJctvMWsykujM1lxHvWyOXs7eif9el+5Hf07pWL60=', NULL, false, 'test_user_19', 'test_user_19@example.com', 'Maria', 'Montgomery', '', '', '', NULL, 'user', '2024-07-19 22:31:31.480531+00', '2026-06-16 19:04:02.508886+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (313, 'pbkdf2_sha256$720000$LdBNUtbMRvhKLKX4NQ3sg4$j4GhA7QkMWwv3B9W+Dg8bM8mDOq/9TxBAV939MLCDQg=', NULL, false, 'test_user_20', 'test_user_20@example.com', 'Michelle', 'Ray', '', '', '', NULL, 'user', '2024-09-07 13:40:15.480531+00', '2026-06-16 19:04:02.508966+00', true, false, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (33, 'pbkdf2_sha256$720000$kqF7SGjJZzG7IoNEvWavbE$umx3V5BsWUQPE0LlsbbFaDgIQ+wDJ2pQhBLTnSH/WHw=', '2026-06-12 06:45:09.051605+00', true, 'admin', 'admin@angotest.com', 'admin', 'admin', '', '', 'España', '2001-01-01', 'admin', '2026-06-12 06:44:01.660948+00', '2026-06-17 21:34:04.179803+00', true, true, NULL);
INSERT INTO public.users (id, password, last_login, is_superuser, username, email, first_name, last_name, phone, address, country, birth_date, role, registered_at, login_at, is_active, is_staff, deleted_at) VALUES (314, 'pbkdf2_sha256$720000$U9HbzbsjFhg423zVbfBXXm$hMqpN3ljC/mheAEJnrm0tLxsgxXjIf4xIB0wzmd0qRI=', NULL, false, 'jaterli', 'jaterli@hotmail.com', 'Jaime', 'Terciado', '655998855', 'Calle Mayor, 23', 'España', '2000-10-10', 'user', '2026-06-16 21:15:52.31463+00', '2026-06-16 21:16:06.069022+00', true, false, NULL);


--
-- Data for Name: tests; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (517, 'Física: Mecánica Clásica', 'Test sobre principios fundamentales de mecánica clásica y leyes de Newton', 'Ciencias', 'Física', 'Mecánica clásica', 'Intermedio', '2025-10-16 09:03:12+00', '2026-06-16 17:19:33.720311+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (520, 'Química: Química Orgánica', 'Test sobre compuestos orgánicos, grupos funcionales y nomenclatura', 'Ciencias', 'Química', 'Química orgánica', 'Avanzado', '2024-01-26 16:00:48+00', '2026-06-16 17:19:33.723881+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (523, 'Música: Acordes', 'Test sobre teoría musical, formación de acordes y progresiones', 'Música', 'Teoría Musical', 'Acordes', 'Intermedio', '2024-09-07 13:07:36+00', '2026-06-16 17:19:33.726985+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (526, 'Álgebra: Ecuaciones Cuadráticas', 'Test sobre ecuaciones de segundo grado y sus métodos de resolución', 'Matemáticas', 'Álgebra', 'Ecuaciones cuadráticas', 'Intermedio', '2024-05-22 08:43:54+00', '2026-06-16 17:19:33.731427+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (529, 'Historia Moderna: Revolución Francesa', 'Test sobre la Revolución Francesa y sus eventos principales', 'Historia', 'Historia Moderna', 'Revolución Francesa', 'Intermedio', '2025-11-24 01:51:22+00', '2026-06-16 17:19:33.734763+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (532, 'Cloud Computing: AWS Fundamentals', 'Test sobre conceptos básicos de Amazon Web Services y servicios de nube', 'Tecnología', 'Cloud Computing', 'AWS Fundamentals', 'Principiante', '2024-03-31 02:29:57+00', '2026-06-16 17:19:33.73772+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (535, 'Blockchain: Smart Contracts', 'Test sobre contratos inteligentes y su funcionamiento en blockchain', 'Tecnología', 'Blockchain', 'Smart Contracts', 'Avanzado', '2025-03-08 07:09:25+00', '2026-06-16 17:19:33.740665+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (515, 'Álgebra: Ecuaciones Lineales 2', 'Test sobre ecuaciones lineales con una incógnita y sus aplicaciones', 'Matemáticas', 'Álgebra', 'Ecuaciones lineales', 'Principiante', '2024-01-31 09:24:40+00', '2026-06-16 17:19:33.743745+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (518, 'JavaScript: DOM Manipulation', 'Test sobre manipulación del Document Object Model con JavaScript', 'Programación', 'JavaScript', 'DOM Manipulation', 'Intermedio', '2024-08-11 13:28:15+00', '2026-06-16 17:19:33.749445+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (521, 'Inglés: Phrasal Verbs', 'Test sobre verbos frasales comunes en inglés y su uso en contexto', 'Idiomas', 'Inglés', 'Phrasal Verbs', 'Intermedio', '2025-06-02 02:55:07+00', '2026-06-16 17:19:33.753197+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (524, 'Ciberseguridad: Seguridad de Redes', 'Test sobre fundamentos de seguridad en redes informáticas', 'Tecnología', 'Ciberseguridad', 'Seguridad de redes', 'Avanzado', '2024-01-29 02:26:03+00', '2026-06-16 17:19:33.756545+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (527, 'Python: Funciones', 'Test sobre funciones en Python, parámetros y valores de retorno', 'Programación', 'Python', 'Funciones', 'Intermedio', '2024-07-23 04:39:41+00', '2026-06-16 17:19:33.761204+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (530, 'Biología: Genética', 'Test sobre conceptos básicos de genética y herencia', 'Ciencias', 'Biología', 'Genética', 'Intermedio', '2025-12-20 01:50:26+00', '2026-06-16 17:19:33.764787+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (533, 'Macroeconomía: Inflación', 'Test sobre inflación, causas y efectos en la economía', 'Economía', 'Macroeconomía', 'Inflación', 'Intermedio', '2025-03-05 14:01:33+00', '2026-06-16 17:19:33.768145+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (538, 'Segunda Guerra Mundial: Desafíos y Eventos', 'Evaluación de conocimientos sobre la Segunda Guerra Mundial, abordando aspectos clave y eventos cruciales.', 'Historia', 'Historia Contemporánea', 'Segunda Guerra Mundial', 'Avanzado', '2026-06-16 21:05:34.758055+00', '2026-06-16 21:05:34.758069+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (539, 'Phrasal Verbs Básicos en Inglés', 'Evalúa tus conocimientos de phrasal verbs comunes en inglés para principiantes.', 'Idiomas', 'Inglés', 'Phrasal Verbs', 'Principiante', '2026-06-16 21:16:29.860502+00', '2026-06-16 21:16:29.86053+00', true, 314);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (516, 'Python: Sintaxis Básica', 'Test sobre los fundamentos de la sintaxis de Python para programación', 'Programación', 'Python', 'Sintaxis básica', 'Principiante', '2025-04-05 02:27:16+00', '2026-06-16 17:19:33.771544+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (519, 'Historia Antigua: Imperio Romano', 'Test sobre la historia del Imperio Romano y su legado', 'Historia', 'Historia Antigua', 'Imperio Romano', 'Intermedio', '2024-10-11 05:14:11+00', '2026-06-16 17:19:33.77477+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (522, 'Finanzas Personales: Presupuestos', 'Test sobre gestión de presupuestos y finanzas personales', 'Economía', 'Finanzas Personales', 'Presupuestos', 'Principiante', '2026-02-16 11:48:46+00', '2026-06-16 17:19:33.777901+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (525, 'Productividad: Método Pomodoro', 'Test sobre la técnica Pomodoro para mejorar la productividad y gestión del tiempo', 'Desarrollo Personal', 'Productividad', 'Método Pomodoro', 'Principiante', '2025-12-15 21:23:12+00', '2026-06-16 17:19:33.78134+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (528, 'Cálculo: Derivadas', 'Test sobre derivadas y sus aplicaciones en cálculo diferencial', 'Matemáticas', 'Cálculo', 'Derivadas', 'Avanzado', '2024-12-14 16:07:01+00', '2026-06-16 17:19:33.784793+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (531, 'Guitarra: Acordes Básicos', 'Test sobre acordes básicos y técnicas para principiantes en guitarra', 'Música', 'Guitarra', 'Acordes básicos', 'Principiante', '2024-06-08 12:50:21+00', '2026-06-16 17:19:33.788184+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (534, 'Comunicación: Hablar en Público', 'Test sobre técnicas y habilidades para hablar efectivamente en público', 'Desarrollo Personal', 'Comunicación', 'Hablar en público', 'Principiante', '2026-02-20 18:15:18+00', '2026-06-16 17:19:33.791418+00', true, 33);
INSERT INTO public.tests (id, title, description, main_topic, sub_topic, specific_topic, level, created_at, updated_at, is_active, created_by_id) VALUES (540, 'Trading Avanzado en Mercados Financieros', 'Preguntas avanzadas sobre trading y mercados financieros', 'Economía', 'Mercados Financieros', 'Trading', 'Intermedio', '2026-06-18 14:52:49.999445+00', '2026-06-18 14:55:08.981373+00', true, 33);


--
-- Data for Name: ai_request_logs; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (1, 'Ciencias', 'Física', 'Termodinámica', 'Intermedio', 10, 3, 'en', 'structured', '', '{}', 'groq', 'llama-3.1-8b-instant', 'failed', '401 Client Error: Unauthorized for url: https://api.groq.com/openai/v1/chat/completions', 0, 0, '2026-06-16 20:19:51.626298+00', '2026-06-16 20:19:51.831683+00', NULL, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (2, 'Ciencias', 'Física', 'Termodinámica', 'Intermedio', 10, 3, 'en', 'structured', '', '{}', 'groq', 'llama-3.1-8b-instant', 'failed', '401 Client Error: Unauthorized for url: https://api.groq.com/openai/v1/chat/completions', 0, 0, '2026-06-16 20:24:22.890081+00', '2026-06-16 20:24:23.063468+00', NULL, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (3, 'Ciencias', 'Física', 'Termodinámica', 'Intermedio', 10, 3, 'en', 'structured', '', '{}', 'groq', 'llama-3.1-8b-instant', 'failed', '413 Client Error: Payload Too Large for url: https://api.groq.com/openai/v1/chat/completions', 0, 0, '2026-06-16 20:28:52.184401+00', '2026-06-16 20:28:52.328638+00', NULL, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (4, 'Ciencias', 'Física', 'Termodinámica', 'Intermedio', 10, 3, 'en', 'structured', '', '{}', 'groq', 'llama-3.1-8b-instant', 'failed', '413 Client Error: Payload Too Large for url: https://api.groq.com/openai/v1/chat/completions', 0, 0, '2026-06-16 20:37:50.661627+00', '2026-06-16 20:37:50.826843+00', NULL, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (5, 'Ciencias', 'Física', 'Termodinámica', 'Intermedio', 10, 3, 'en', 'structured', '', '{}', 'groq', 'groq/compound', 'failed', '403 Client Error: Forbidden for url: https://api.groq.com/openai/v1/chat/completions', 0, 0, '2026-06-16 20:41:35.838072+00', '2026-06-16 20:41:39.062343+00', NULL, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (6, 'Ciencias', 'Química', 'Química orgánica', 'Intermedio', 10, 3, 'en', 'structured', '', '{}', 'groq', 'groq/compound', 'failed', '403 Client Error: Forbidden for url: https://api.groq.com/openai/v1/chat/completions', 0, 0, '2026-06-16 20:51:22.485558+00', '2026-06-16 20:51:25.73559+00', NULL, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (7, 'Ciencias', 'Química', 'Química orgánica', 'Intermedio', 10, 3, 'en', 'structured', '', '{}', 'groq', 'groq/compound', 'failed', '403 Client Error: Forbidden for url: https://api.groq.com/openai/v1/chat/completions', 0, 0, '2026-06-16 20:57:06.895243+00', '2026-06-16 20:57:10.105145+00', NULL, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (8, 'Ciencias', 'Química', 'Química orgánica', 'Intermedio', 10, 3, 'en', 'structured', '', '{}', 'groq', 'meta-llama/llama-4-scout-17b-16e-instruct', 'failed', '403 Client Error: Forbidden for url: https://api.groq.com/openai/v1/chat/completions', 0, 0, '2026-06-16 20:59:59.548307+00', '2026-06-16 20:59:59.701707+00', NULL, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (9, 'Ciencias', 'Química', 'Química orgánica', 'Intermedio', 10, 3, 'en', 'structured', '', '{"id": "chatcmpl-4f10efc4-dbcf-4d8d-8350-ef5cd5ef907e", "model": "meta-llama/llama-4-scout-17b-16e-instruct", "usage": {"queue_time": 0.016767798, "total_time": 1.908355169, "prompt_time": 0.009047687, "total_tokens": 1038, "prompt_tokens": 196, "completion_time": 1.899307482, "completion_tokens": 842}, "object": "chat.completion", "x_groq": {"id": "req_01kv93wt3bfy18zzvhx02nn3np", "seed": 1005918263}, "choices": [{"index": 0, "message": {"role": "assistant", "content": "```json\n{\n  \"title\": \"Organic Chemistry Test\",\n  \"description\": \"A 10-question test on organic chemistry for intermediate-level students.\",\n  \"questions\": [\n    {\n      \"question_text\": \"What is the primary functional group present in alcohols?\",\n      \"answers\": [\n        {\"answer_text\": \"Carboxyl group\", \"is_correct\": false},\n        {\"answer_text\": \"Hydroxyl group\", \"is_correct\": true},\n        {\"answer_text\": \"Carbonyl group\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"Which of the following types of reactions involves the addition of a molecule across a double bond?\",\n      \"answers\": [\n        {\"answer_text\": \"Substitution reaction\", \"is_correct\": false},\n        {\"answer_text\": \"Elimination reaction\", \"is_correct\": false},\n        {\"answer_text\": \"Addition reaction\", \"is_correct\": true}\n      ]\n    },\n    {\n      \"question_text\": \"What is the term for a compound that has the same molecular formula but a different structural formula?\",\n      \"answers\": [\n        {\"answer_text\": \"Isomer\", \"is_correct\": true},\n        {\"answer_text\": \"Homolog\", \"is_correct\": false},\n        {\"answer_text\": \"Polymer\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"Which of the following organic compounds is an example of a saturated hydrocarbon?\",\n      \"answers\": [\n        {\"answer_text\": \"Ethene\", \"is_correct\": false},\n        {\"answer_text\": \"Methane\", \"is_correct\": true},\n        {\"answer_text\": \"Benzene\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"What is the name of the reaction that converts an alkene to an alkane?\",\n      \"answers\": [\n        {\"answer_text\": \"Hydrogenation\", \"is_correct\": true},\n        {\"answer_text\": \"Halogenation\", \"is_correct\": false},\n        {\"answer_text\": \"Oxidation\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"Which of the following functional groups is characteristic of a ketone?\",\n      \"answers\": [\n        {\"answer_text\": \"Aldehyde group\", \"is_correct\": false},\n        {\"answer_text\": \"Carbonyl group\", \"is_correct\": true},\n        {\"answer_text\": \"Ester group\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"What is the term for the process of heating a compound to produce a smaller molecule?\",\n      \"answers\": [\n        {\"answer_text\": \"Cracking\", \"is_correct\": true},\n        {\"answer_text\": \"Polymerization\", \"is_correct\": false},\n        {\"answer_text\": \"Hydrogenation\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"Which of the following types of compounds is known for its ability to form hydrogen bonds?\",\n      \"answers\": [\n        {\"answer_text\": \"Alkanes\", \"is_correct\": false},\n        {\"answer_text\": \"Alcohols\", \"is_correct\": true},\n        {\"answer_text\": \"Ethers\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"What is the name of the reaction that involves the replacement of a functional group with another functional group?\",\n      \"answers\": [\n        {\"answer_text\": \"Substitution reaction\", \"is_correct\": true},\n        {\"answer_text\": \"Elimination reaction\", \"is_correct\": false},\n        {\"answer_text\": \"Addition reaction\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"Which of the following organic compounds is an example of an aromatic hydrocarbon?\",\n      \"answers\": [\n        {\"answer_text\": \"Cyclohexane\", \"is_correct\": false},\n        {\"answer_text\": \"Benzene\", \"is_correct\": true},\n        {\"answer_text\": \"Methane\", \"is_correct\": false}\n      ]\n    }\n  ]\n}\n```"}, "logprobs": null, "finish_reason": "stop"}], "created": 1781643767, "service_tier": "on_demand", "usage_breakdown": null, "system_fingerprint": "fp_ec4c899792"}', 'groq', 'meta-llama/llama-4-scout-17b-16e-instruct', 'completed', '', 2.120865821838379, 1038, '2026-06-16 21:02:45.870847+00', '2026-06-16 21:02:48.020862+00', NULL, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (10, 'Historia', 'Historia Contemporánea', 'Segunda Guerra Mundial', 'Avanzado', 10, 3, 'es', 'structured', '', '{"id": "chatcmpl-b9ce7184-6ec1-473d-94fe-19da091d66df", "model": "meta-llama/llama-4-scout-17b-16e-instruct", "usage": {"queue_time": 0.248842369, "total_time": 2.120950682, "prompt_time": 0.013750018, "total_tokens": 1133, "prompt_tokens": 200, "completion_time": 2.107200664, "completion_tokens": 933}, "object": "chat.completion", "x_groq": {"id": "req_01kv941wceev9bbygtfp5d1xdb", "seed": 1805156411}, "choices": [{"index": 0, "message": {"role": "assistant", "content": "```json\n{\n  \"title\": \"Segunda Guerra Mundial: Desafíos y Eventos\",\n  \"description\": \"Evaluación de conocimientos sobre la Segunda Guerra Mundial, abordando aspectos clave y eventos cruciales.\",\n  \"questions\": [\n    {\n      \"question_text\": \"¿Cuál fue el nombre del plan alemán para invadir la Unión Soviética en 1941?\",\n      \"answers\": [\n        {\"answer_text\": \"Operación Barbarroja\", \"is_correct\": true},\n        {\"answer_text\": \"Operación Overlord\", \"is_correct\": false},\n        {\"answer_text\": \"Operación Sea Lion\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Quién fue el líder de la Unión Soviética durante la Segunda Guerra Mundial?\",\n      \"answers\": [\n        {\"answer_text\": \"Iósif Stalin\", \"is_correct\": true},\n        {\"answer_text\": \"Lavrenti Beria\", \"is_correct\": false},\n        {\"answer_text\": \"Viacheslav Molotov\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿En qué año se llevó a cabo la Conferencia de Yalta?\",\n      \"answers\": [\n        {\"answer_text\": \"1945\", \"is_correct\": true},\n        {\"answer_text\": \"1943\", \"is_correct\": false},\n        {\"answer_text\": \"1942\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál fue el nombre del campo de concentración nazi en Polonia donde se estima que murieron más de un millón de personas?\",\n      \"answers\": [\n        {\"answer_text\": \"Auschwitz-Birkenau\", \"is_correct\": true},\n        {\"answer_text\": \"Treblinka\", \"is_correct\": false},\n        {\"answer_text\": \"Buchenwald\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Quién fue el primer ministro del Reino Unido durante la mayor parte de la Segunda Guerra Mundial?\",\n      \"answers\": [\n        {\"answer_text\": \"Winston Churchill\", \"is_correct\": true},\n        {\"answer_text\": \"Neville Chamberlain\", \"is_correct\": false},\n        {\"answer_text\": \"Clement Attlee\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál fue el nombre del bombardero alemán utilizado durante la Batalla de Inglaterra?\",\n      \"answers\": [\n        {\"answer_text\": \"Junkers Ju 87\", \"is_correct\": false},\n        {\"answer_text\": \"Messerschmitt Bf 109\", \"is_correct\": false},\n        {\"answer_text\": \"Heinkel He 111\", \"is_correct\": true}\n      ]\n    },\n    {\n      \"question_text\": \"¿En qué ciudad se llevó a cabo la rendición incondicional de Alemania en 1945?\",\n      \"answers\": [\n        {\"answer_text\": \"Berlín\", \"is_correct\": true},\n        {\"answer_text\": \"París\", \"is_correct\": false},\n        {\"answer_text\": \"Moscú\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Quién fue el líder de la resistencia francesa durante la Segunda Guerra Mundial?\",\n      \"answers\": [\n        {\"answer_text\": \"Charles de Gaulle\", \"is_correct\": true},\n        {\"answer_text\": \"Jean Moulin\", \"is_correct\": false},\n        {\"answer_text\": \"Philippe Pétain\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál fue el nombre del programa de préstamos y arrendamientos implementado por Estados Unidos para ayudar a sus aliados durante la Segunda Guerra Mundial?\",\n      \"answers\": [\n        {\"answer_text\": \"Ley de Préstamos y Arrendamientos\", \"is_correct\": true},\n        {\"answer_text\": \"Plan Marshall\", \"is_correct\": false},\n        {\"answer_text\": \"Acuerdo de Ayuda Mutua\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿En qué fecha comenzó la Segunda Guerra Mundial?\",\n      \"answers\": [\n        {\"answer_text\": \"1 de septiembre de 1939\", \"is_correct\": true},\n        {\"answer_text\": \"3 de septiembre de 1939\", \"is_correct\": false},\n        {\"answer_text\": \"15 de agosto de 1939\", \"is_correct\": false}\n      ]\n    }\n  ]\n}\n```"}, "logprobs": null, "finish_reason": "stop"}], "created": 1781643934, "service_tier": "on_demand", "usage_breakdown": null, "system_fingerprint": "fp_ec4c899792"}', 'groq', 'meta-llama/llama-4-scout-17b-16e-instruct', 'completed', '', 2.593973398208618, 1133, '2026-06-16 21:05:32.159308+00', '2026-06-16 21:05:34.784461+00', 538, 33);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (11, 'Idiomas', 'Inglés', 'Phrasal Verbs', 'Principiante', 10, 3, 'es', 'guided', '', '{"id": "chatcmpl-9b514971-2189-456f-b01f-0f342afe602a", "model": "meta-llama/llama-4-scout-17b-16e-instruct", "usage": {"queue_time": 0.057171004, "total_time": 1.852150287, "prompt_time": 0.013591891, "total_tokens": 1015, "prompt_tokens": 200, "completion_time": 1.838558396, "completion_tokens": 815}, "object": "chat.completion", "x_groq": {"id": "req_01kv94nwmxejj8kfv3j1ekpf8x", "seed": 285279408}, "choices": [{"index": 0, "message": {"role": "assistant", "content": "```json\n{\n  \"title\": \"Phrasal Verbs Básicos en Inglés\",\n  \"description\": \"Evalúa tus conocimientos de phrasal verbs comunes en inglés para principiantes.\",\n  \"questions\": [\n    {\n      \"question_text\": \"¿Qué significa ''pick up''?\",\n      \"answers\": [\n        {\"answer_text\": \"Recoger o tomar algo\", \"is_correct\": true},\n        {\"answer_text\": \"Dejar caer algo\", \"is_correct\": false},\n        {\"answer_text\": \"Comprar algo\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué significa ''get on''?\",\n      \"answers\": [\n        {\"answer_text\": \"Subir a un vehículo\", \"is_correct\": true},\n        {\"answer_text\": \"Bajar de un vehículo\", \"is_correct\": false},\n        {\"answer_text\": \"Conducir un vehículo\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué significa ''turn off''?\",\n      \"answers\": [\n        {\"answer_text\": \"Apagar algo\", \"is_correct\": true},\n        {\"answer_text\": \"Encender algo\", \"is_correct\": false},\n        {\"answer_text\": \"Arreglar algo\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué significa ''put on''?\",\n      \"answers\": [\n        {\"answer_text\": \"Ponerse ropa o algo\", \"is_correct\": true},\n        {\"answer_text\": \"Quitarse ropa o algo\", \"is_correct\": false},\n        {\"answer_text\": \"Romper algo\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué significa ''take off''?\",\n      \"answers\": [\n        {\"answer_text\": \"Quitarse algo o despegar\", \"is_correct\": true},\n        {\"answer_text\": \"Ponerse algo\", \"is_correct\": false},\n        {\"answer_text\": \"Volar alto\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué significa ''give up''?\",\n      \"answers\": [\n        {\"answer_text\": \"Rendirse o abandonar\", \"is_correct\": true},\n        {\"answer_text\": \"Continuar adelante\", \"is_correct\": false},\n        {\"answer_text\": \"Olvidar algo\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué significa ''look after''?\",\n      \"answers\": [\n        {\"answer_text\": \"Cuidar de alguien o algo\", \"is_correct\": true},\n        {\"answer_text\": \"Mirar algo fijamente\", \"is_correct\": false},\n        {\"answer_text\": \"Olvidar algo\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué significa ''go on''?\",\n      \"answers\": [\n        {\"answer_text\": \"Continuar haciendo algo\", \"is_correct\": true},\n        {\"answer_text\": \"Apagarse\", \"is_correct\": false},\n        {\"answer_text\": \"Detenerse\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué significa ''wake up''?\",\n      \"answers\": [\n        {\"answer_text\": \"Despertar\", \"is_correct\": true},\n        {\"answer_text\": \"Dormir profundamente\", \"is_correct\": false},\n        {\"answer_text\": \"Soñar\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué significa ''bring up''?\",\n      \"answers\": [\n        {\"answer_text\": \"Criar o educar a alguien\", \"is_correct\": true},\n        {\"answer_text\": \"Bajar algo\", \"is_correct\": false},\n        {\"answer_text\": \"Olvidar algo\", \"is_correct\": false}\n      ]\n    }\n  ]\n}\n```"}, "logprobs": null, "finish_reason": "stop"}], "created": 1781644589, "service_tier": "on_demand", "usage_breakdown": null, "system_fingerprint": "fp_ec4c899792"}', 'groq', 'meta-llama/llama-4-scout-17b-16e-instruct', 'completed', '', 2.0933756828308105, 1015, '2026-06-16 21:16:27.762162+00', '2026-06-16 21:16:29.948558+00', 539, 314);
INSERT INTO public.ai_request_logs (id, main_topic, sub_topic, specific_topic, level, num_questions, num_answers, language, generation_mode, ai_prompt, ai_response, ai_provider, ai_model, status, error_message, response_time, tokens_used, created_at, updated_at, test_id, user_id) VALUES (12, '', '', '', 'Avanzado', 20, 3, 'es', 'prompt', 'Genera un tema de nivel Avanzado sobre Trading aplicado a los mercados financieros', '{"id": "chatcmpl-9005a0a8-7e94-46ae-b563-86336fd0ea68", "model": "meta-llama/llama-4-scout-17b-16e-instruct", "usage": {"queue_time": 0.131950351, "total_time": 3.9962288150000003, "prompt_time": 0.036243752, "total_tokens": 2498, "prompt_tokens": 749, "completion_time": 3.959985063, "completion_tokens": 1749}, "object": "chat.completion", "x_groq": {"id": "req_01kvdkgq2qfqkv0wdzwda7cb15", "seed": 642430336}, "choices": [{"index": 0, "message": {"role": "assistant", "content": "```json\n{\n  \"title\": \"Trading Avanzado en Mercados Financieros\",\n  \"description\": \"Preguntas avanzadas sobre trading y mercados financieros\",\n  \"main_topic\": \"Economía\",\n  \"sub_topic\": \"Finanzas\",\n  \"specific_topic\": \"Trading\",\n  \"questions\": [\n    {\n      \"question_text\": \"¿Cuál es el objetivo principal de un stop-loss en trading?\",\n      \"answers\": [\n        {\"answer_text\": \"Maximizar las ganancias\", \"is_correct\": false},\n        {\"answer_text\": \"Limitar las pérdidas\", \"is_correct\": true},\n        {\"answer_text\": \"Incrementar el leverage\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué tipo de análisis se enfoca en estudiar gráficos y patrones de precios?\",\n      \"answers\": [\n        {\"answer_text\": \"Análisis fundamental\", \"is_correct\": false},\n        {\"answer_text\": \"Análisis técnico\", \"is_correct\": true},\n        {\"answer_text\": \"Análisis cuantitativo\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál es el nombre del indicador que mide la velocidad y el cambio de un movimiento de precio?\",\n      \"answers\": [\n        {\"answer_text\": \"MACD\", \"is_correct\": false},\n        {\"answer_text\": \"RSI\", \"is_correct\": false},\n        {\"answer_text\": \"Momentum\", \"is_correct\": true}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué estrategia de trading implica comprar y vender instrumentos financieros dentro de un mismo día?\",\n      \"answers\": [\n        {\"answer_text\": \"Swing trading\", \"is_correct\": false},\n        {\"answer_text\": \"Day trading\", \"is_correct\": true},\n        {\"answer_text\": \"Position trading\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál es el término que describe la relación entre dos pares de divisas que se mueven en direcciones opuestas?\",\n      \"answers\": [\n        {\"answer_text\": \"Correlación positiva\", \"is_correct\": false},\n        {\"answer_text\": \"Correlación negativa\", \"is_correct\": true},\n        {\"answer_text\": \"Correlación neutra\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué tipo de orden se ejecuta a un precio específico en el mercado?\",\n      \"answers\": [\n        {\"answer_text\": \"Orden de mercado\", \"is_correct\": false},\n        {\"answer_text\": \"Orden limitada\", \"is_correct\": true},\n        {\"answer_text\": \"Orden stop\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál es el indicador que muestra la tendencia y la fuerza de un movimiento de precio mediante medias móviles?\",\n      \"answers\": [\n        {\"answer_text\": \"Bollinger Bands\", \"is_correct\": false},\n        {\"answer_text\": \"Ichimoku Cloud\", \"is_correct\": true},\n        {\"answer_text\": \"Stochastic Oscillator\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué estrategia de trading implica seguir la tendencia principal del mercado?\",\n      \"answers\": [\n        {\"answer_text\": \"Contrarian\", \"is_correct\": false},\n        {\"answer_text\": \"Trend following\", \"is_correct\": true},\n        {\"answer_text\": \"Range trading\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál es el término que describe la aversión al riesgo en los mercados financieros?\",\n      \"answers\": [\n        {\"answer_text\": \"Aversión a la pérdida\", \"is_correct\": false},\n        {\"answer_text\": \"Tolerancia al riesgo\", \"is_correct\": false},\n        {\"answer_text\": \"Aversión al riesgo\", \"is_correct\": true}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué tipo de análisis se enfoca en estudiar los estados financieros y la economía de un país?\",\n      \"answers\": [\n        {\"answer_text\": \"Análisis técnico\", \"is_correct\": false},\n        {\"answer_text\": \"Análisis fundamental\", \"is_correct\": true},\n        {\"answer_text\": \"Análisis cuantitativo\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál es el nombre del patrón de reversión que se forma con una vela verde seguida de una vela roja?\",\n      \"answers\": [\n        {\"answer_text\": \"Martillo\", \"is_correct\": false},\n        {\"answer_text\": \"Estrella fugaz\", \"is_correct\": false},\n        {\"answer_text\": \"Tumba de toro\", \"is_correct\": true}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué tipo de trading implica mantener posiciones durante un período prolongado de tiempo?\",\n      \"answers\": [\n        {\"answer_text\": \"Day trading\", \"is_correct\": false},\n        {\"answer_text\": \"Swing trading\", \"is_correct\": false},\n        {\"answer_text\": \"Position trading\", \"is_correct\": true}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál es el término que describe la relación entre el tamaño de una posición y el capital total de una cuenta de trading?\",\n      \"answers\": [\n        {\"answer_text\": \"Leverage\", \"is_correct\": false},\n        {\"answer_text\": \"Margen\", \"is_correct\": false},\n        {\"answer_text\": \"Exposición\", \"is_correct\": true}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué indicador mide la volatilidad de un activo financiero?\",\n      \"answers\": [\n        {\"answer_text\": \"Media móvil\", \"is_correct\": false},\n        {\"answer_text\": \"Bollinger Bands\", \"is_correct\": true},\n        {\"answer_text\": \"RSI\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué tipo de orden se ejecuta cuando el precio de mercado alcanza un nivel específico?\",\n      \"answers\": [\n        {\"answer_text\": \"Orden de mercado\", \"is_correct\": false},\n        {\"answer_text\": \"Orden limitada\", \"is_correct\": false},\n        {\"answer_text\": \"Orden stop\", \"is_correct\": true}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál es el término que describe la capacidad de un mercado para absorber grandes órdenes de compra o venta sin afectar significativamente el precio?\",\n      \"answers\": [\n        {\"answer_text\": \"Liquidez\", \"is_correct\": true},\n        {\"answer_text\": \"Volatilidad\", \"is_correct\": false},\n        {\"answer_text\": \"Profundidad\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué estrategia de trading implica vender un instrumento financiero que no se posee con la expectativa de comprarlo de nuevo a un precio más bajo?\",\n      \"answers\": [\n        {\"answer_text\": \"Compraventa\", \"is_correct\": false},\n        {\"answer_text\": \"Venta en corto\", \"is_correct\": true},\n        {\"answer_text\": \"Cobertura\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál es el término que describe la tendencia de un mercado a moverse en una dirección específica?\",\n      \"answers\": [\n        {\"answer_text\": \"Tendencia\", \"is_correct\": true},\n        {\"answer_text\": \"Reversión\", \"is_correct\": false},\n        {\"answer_text\": \"Consolidación\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Qué tipo de análisis se enfoca en estudiar los patrones y tendencias en los datos históricos de un mercado?\",\n      \"answers\": [\n        {\"answer_text\": \"Análisis fundamental\", \"is_correct\": false},\n        {\"answer_text\": \"Análisis técnico\", \"is_correct\": true},\n        {\"answer_text\": \"Análisis cuantitativo\", \"is_correct\": false}\n      ]\n    },\n    {\n      \"question_text\": \"¿Cuál es el término que describe la diferencia entre el precio de compra y venta de un instrumento financiero?\",\n      \"answers\": [\n        {\"answer_text\": \"Spread\", \"is_correct\": true},\n        {\"answer_text\": \"Comisión\", \"is_correct\": false},\n        {\"answer_text\": \"Swap\", \"is_correct\": false}\n      ]\n    }\n  ]\n}\n```"}, "logprobs": null, "finish_reason": "stop"}], "created": 1781794368, "service_tier": "on_demand", "usage_breakdown": null, "system_fingerprint": "fp_2f97044c6d"}', 'groq', 'meta-llama/llama-4-scout-17b-16e-instruct', 'completed', '', 4.505293130874634, 2498, '2026-06-18 14:52:45.487703+00', '2026-06-18 14:52:50.042404+00', 540, 33);


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.questions (id, question_text, test_id) VALUES (4912, '¿Qué significa ''give up''?', 521);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4913, '¿Cuál es el phrasal verb para ''continuar''?', 521);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4914, '¿Qué significa ''look after''?', 521);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4915, '¿Cómo se dice ''posponer'' en inglés con un phrasal verb?', 521);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4916, '¿Qué significa ''break down''?', 521);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4917, '¿Cuál es el phrasal verb para ''descubrir''?', 521);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4918, '¿Qué significa ''take off''?', 521);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4919, '¿Cómo se dice ''esperar con ansias'' en inglés con un phrasal verb?', 521);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4964, '¿Cómo se define una función en Python?', 527);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4858, '¿Cuál es el valor de x en la ecuación 3x + 7 = 22?', 515);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4859, '¿Qué significa resolver una ecuación lineal?', 515);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4860, '¿Cuál es la forma general de una ecuación lineal?', 515);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4861, 'Resuelve: 2(x - 3) = 8', 515);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4862, '¿Qué propiedad se usa para resolver 2x = 10?', 515);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4863, '¿Cuántas soluciones tiene una ecuación lineal de primer grado?', 515);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4864, 'Resuelve: x/4 - 2 = 3', 515);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4865, '¿Qué operación inversa se usa para eliminar la suma en x + 5 = 9?', 515);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4866, 'Si 3x - 5 = 16, ¿cuánto vale x?', 515);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4965, '¿Qué palabra clave se usa para retornar un valor en una función?', 527);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4966, '¿Qué son los parámetros en una función?', 527);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4967, '¿Cuál es la salida de len(''Python'')?', 527);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4968, '¿Qué hace la función range(5)?', 527);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4969, '¿Qué es el ámbito de una variable en una función?', 527);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4970, '¿Cómo se llama una función recursiva?', 527);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4971, '¿Qué devuelve una función si no tiene return?', 527);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5012, '¿Qué es la inflación?', 533);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5013, '¿Qué índice mide la inflación?', 533);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5014, '¿Cuál es una causa común de inflación?', 533);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5015, '¿Qué es la hiperinflación?', 533);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5016, '¿Cómo afecta la inflación al ahorro?', 533);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5017, '¿Qué organismo generalmente combate la inflación?', 533);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5018, '¿Qué es la deflación?', 533);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5019, '¿Qué instrumento usa el banco central para controlar la inflación?', 533);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5057, '¿Qué significa ''pick up''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5058, '¿Qué significa ''get on''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5059, '¿Qué significa ''turn off''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5060, '¿Qué significa ''put on''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5061, '¿Qué significa ''take off''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5062, '¿Qué significa ''give up''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5063, '¿Qué significa ''look after''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5064, '¿Qué significa ''go on''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5065, '¿Qué significa ''wake up''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5066, '¿Qué significa ''bring up''?', 539);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4867, '¿Cómo se escribe un comentario en Python?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4868, '¿Cuál es la salida de print(2 ** 3)?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4869, '¿Qué tipo de dato es True en Python?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4870, '¿Cuál es la forma correcta de definir una lista en Python?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4871, '¿Qué función se usa para convertir un texto a número entero?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4872, '¿Cómo se verifica si un número es mayor que otro en Python?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4873, '¿Qué operador se usa para concatenar strings?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4874, '¿Cuál es la salida de len(''Hola Mundo'')?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4875, '¿Cómo se declara una variable en Python?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4876, '¿Qué tipo de bucle se usa para iterar sobre una secuencia?', 516);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4920, '¿Qué es un presupuesto personal?', 522);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4921, '¿Cuál es la regla del 50/30/20?', 522);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4922, '¿Qué diferencia hay entre un gasto fijo y variable?', 522);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4923, '¿Qué porcentaje del ingreso se recomienda destinar al ahorro?', 522);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4924, '¿Qué es un fondo de emergencia?', 522);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4925, '¿Qué herramienta ayuda a controlar los gastos diarios?', 522);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4926, '¿Qué se considera un ingreso pasivo?', 522);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4927, '¿Cuánto tiempo de gastos debe cubrir un fondo de emergencia ideal?', 522);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4972, '¿Qué representa la derivada de una función en un punto?', 528);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4973, '¿Cuál es la derivada de f(x) = x³?', 528);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4974, '¿Qué regla se usa para derivar el producto de dos funciones?', 528);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4975, '¿Cuál es la derivada de f(x) = sen(x)?', 528);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4976, '¿Qué es un punto crítico en una función?', 528);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4977, '¿Cuál es la derivada de f(x) = eˣ?', 528);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4978, '¿Qué teorema relaciona derivada y monotonía?', 528);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4979, '¿Cuál es la segunda derivada de f(x) = x⁴?', 528);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5020, '¿Cuál es la clave para una buena presentación oral?', 534);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5021, '¿Qué importancia tiene el lenguaje corporal al hablar en público?', 534);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5022, '¿Cómo se maneja el nerviosismo antes de hablar en público?', 534);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5023, '¿Cuál es la estructura básica de un discurso?', 534);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5024, '¿Qué se debe hacer con los nervios durante una presentación?', 534);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5025, '¿Cuánto tiempo debe durar una presentación efectiva?', 534);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5026, '¿Qué función cumplen las pausas en un discurso?', 534);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5027, '¿Qué tono de voz se recomienda al hablar en público?', 534);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5067, '¿Cuál es el objetivo principal de un stop-loss en trading?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5068, '¿Qué tipo de análisis se enfoca en estudiar gráficos y patrones de precios?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5069, '¿Cuál es el nombre del indicador que mide la velocidad y el cambio de un movimiento de precio?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5070, '¿Qué estrategia de trading implica comprar y vender instrumentos financieros dentro de un mismo día?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5071, '¿Cuál es el término que describe la relación entre dos pares de divisas que se mueven en direcciones opuestas?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5072, '¿Qué tipo de orden se ejecuta a un precio específico en el mercado?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5073, '¿Cuál es el indicador que muestra la tendencia y la fuerza de un movimiento de precio mediante medias móviles?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5074, '¿Qué estrategia de trading implica seguir la tendencia principal del mercado?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5075, '¿Cuál es el término que describe la aversión al riesgo en los mercados financieros?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5076, '¿Qué tipo de análisis se enfoca en estudiar los estados financieros y la economía de un país?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5077, '¿Cuál es el nombre del patrón de reversión que se forma con una vela verde seguida de una vela roja?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5078, '¿Qué tipo de trading implica mantener posiciones durante un período prolongado de tiempo?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5079, '¿Cuál es el término que describe la relación entre el tamaño de una posición y el capital total de una cuenta de trading?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4877, '¿Qué establece la primera ley de Newton?', 517);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4878, '¿Cuál es la fórmula de la segunda ley de Newton?', 517);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4879, '¿Cómo se llama la fuerza que se opone al movimiento entre dos superficies?', 517);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4880, '¿Qué es la inercia?', 517);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4881, 'Si un objeto tiene una masa de 10 kg y se le aplica una fuerza de 50 N, ¿cuál es su aceleración?', 517);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4882, '¿Cuál es la unidad de medida de la fuerza en el SI?', 517);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4883, '¿Qué establece la tercera ley de Newton?', 517);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4884, '¿Qué tipo de movimiento describe un objeto que cae libremente?', 517);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4885, '¿Cuánto pesa un objeto de 5 kg en la superficie de la Tierra (g = 9.8 m/s²)?', 517);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4928, '¿Cuántas notas tiene un acorde tríada?', 523);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4929, '¿Qué notas forman un acorde mayor?', 523);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4930, '¿Cuál es el acorde relativo menor de Do mayor?', 523);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4931, '¿Qué significa una séptima en un acorde?', 523);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4932, '¿Cómo se escribe un acorde de séptima de dominante en Do?', 523);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4933, '¿Qué es una inversión de acorde?', 523);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4934, '¿Cuántas inversiones tiene una tríada?', 523);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4935, '¿Qué acorde se construye con tónica, tercera menor y quinta justa?', 523);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4980, '¿En qué año comenzó la Revolución Francesa?', 529);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4981, '¿Qué evento marcó el inicio de la Revolución Francesa?', 529);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4982, '¿Qué lema representa la Revolución Francesa?', 529);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4983, '¿Quién fue ejecutado en la guillotina durante la revolución?', 529);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4984, '¿Qué periodo fue conocido como el ''Reinado del Terror''?', 529);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4985, '¿Quién lideró el Comité de Salvación Pública?', 529);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4986, '¿Qué documento declaró los derechos humanos en Francia?', 529);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4987, '¿Qué régimen político sucedió a la Convención Nacional?', 529);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5028, '¿Qué es un smart contract?', 535);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5029, '¿En qué red se ejecutan principalmente los smart contracts?', 535);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5030, '¿Qué lenguaje se usa para escribir smart contracts en Ethereum?', 535);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5031, '¿Qué ventaja principal ofrecen los smart contracts?', 535);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5032, '¿Qué es una DApp?', 535);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5033, '¿Qué problema resuelven los smart contracts?', 535);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5034, '¿Qué es el gas en Ethereum?', 535);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5035, '¿Los smart contracts pueden ser modificados después de desplegados?', 535);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5080, '¿Qué indicador mide la volatilidad de un activo financiero?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5081, '¿Qué tipo de orden se ejecuta cuando el precio de mercado alcanza un nivel específico?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5082, '¿Cuál es el término que describe la capacidad de un mercado para absorber grandes órdenes de compra o venta sin afectar significativamente el precio?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5083, '¿Qué estrategia de trading implica vender un instrumento financiero que no se posee con la expectativa de comprarlo de nuevo a un precio más bajo?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5084, '¿Cuál es el término que describe la tendencia de un mercado a moverse en una dirección específica?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5085, '¿Qué tipo de análisis se enfoca en estudiar los patrones y tendencias en los datos históricos de un mercado?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5086, '¿Cuál es el término que describe la diferencia entre el precio de compra y venta de un instrumento financiero?', 540);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4886, '¿Qué método se usa para seleccionar un elemento por su ID en JavaScript?', 518);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4887, '¿Cómo se cambia el texto de un elemento HTML con JavaScript?', 518);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4888, '¿Qué método permite crear un nuevo elemento HTML?', 518);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4889, '¿Cómo se añade un evento click a un elemento?', 518);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4890, '¿Qué propiedad se usa para obtener el valor de un input?', 518);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4891, '¿Cómo se seleccionan todos los elementos con una clase específica?', 518);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4892, '¿Qué método elimina un elemento del DOM?', 518);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4893, '¿Cómo se agrega una clase CSS a un elemento?', 518);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4894, '¿Cuál es el objeto global en el navegador?', 518);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4936, '¿Qué es un firewall?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4937, '¿Qué protocolo se usa para la transmisión segura de datos?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4938, '¿Qué ataque consiste en enviar múltiples peticiones para saturar un servidor?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4939, '¿Cuál es la función de un certificado SSL/TLS?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4940, '¿Qué es una VLAN?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4941, '¿Qué técnica de ataque utiliza ingeniería social?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4942, '¿Qué es una VPN?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4943, '¿Qué puerto se usa para HTTPS?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4944, '¿Qué tipo de autenticación usa dos factores?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4945, '¿Qué significa IDS en seguridad de redes?', 524);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4988, '¿Qué es un gen?', 530);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4989, '¿Cuántos cromosomas tiene una célula humana normal?', 530);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4990, '¿Qué es el ADN?', 530);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4991, '¿Qué ley establece que cada rasgo se hereda de manera independiente?', 530);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4992, '¿Cómo se llama el proceso de división celular que produce gametos?', 530);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4993, '¿Qué es un alelo?', 530);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4994, '¿Qué diferencia hay entre genotipo y fenotipo?', 530);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4995, '¿Qué estructura contiene toda la información genética de una célula?', 530);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4895, '¿Quién fue el primer emperador romano?', 519);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4896, '¿En qué año cayó el Imperio Romano de Occidente?', 519);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4897, '¿Qué idioma hablaban los romanos en la antigüedad?', 519);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4898, '¿Cuál fue la principal obra arquitectónica romana para el entretenimiento?', 519);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4899, '¿Qué general romano cruzó el Rubicón?', 519);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4900, '¿Cómo se llamaba el sistema de caminos romanos?', 519);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4901, '¿Qué religión se hizo oficial en el Imperio Romano durante el reinado de Teodosio?', 519);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4902, '¿Cómo se llamaba el Senado romano?', 519);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4946, '¿Cuánto dura un ciclo Pomodoro estándar?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4947, '¿Cuánto tiempo de descanso se toma después de un Pomodoro?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4948, '¿Cuántos Pomodoros se recomienda hacer antes de un descanso largo?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4949, '¿Cuál es el objetivo principal del método Pomodoro?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4950, '¿Qué herramienta se usa para aplicar el método Pomodoro?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4951, '¿Qué debe hacer si te interrumpen durante un Pomodoro?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4952, '¿Cuál es el tiempo recomendado para un descanso largo?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4953, '¿Quién creó el método Pomodoro?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4954, '¿Qué significa la palabra ''Pomodoro''?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4955, '¿Qué se recomienda hacer durante el descanso corto?', 525);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4996, '¿Cuáles son los acordes más básicos en guitarra?', 531);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4997, '¿Cómo se forma un acorde mayor en la guitarra?', 531);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4998, '¿Qué dedo se usa para el traste 1 en el acorde de Do mayor?', 531);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4999, '¿Qué significa ''cejilla'' en guitarra?', 531);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5000, '¿Cómo se llama el acorde formado por las cuerdas al aire?', 531);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5001, '¿Qué diferencia hay entre un acorde mayor y uno menor?', 531);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5002, '¿Cuántas cuerdas tiene una guitarra estándar?', 531);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5003, '¿Qué acorde se toca con un solo dedo en el traste 3 de la quinta cuerda?', 531);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4903, '¿Qué grupo funcional caracteriza a los alcoholes?', 520);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4904, '¿Cuál es la fórmula de la glucosa?', 520);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4905, '¿Qué tipo de reacción convierte un alqueno en alcano?', 520);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4906, '¿Cómo se llama el compuesto CH3-CH2-CH2-CH3?', 520);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4907, '¿Qué grupo funcional caracteriza a los ácidos carboxílicos?', 520);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4908, '¿Qué es un hidrocarburo aromático?', 520);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4909, '¿Cuál es la fórmula del benceno?', 520);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4910, '¿Qué reacción caracteriza a los compuestos carbonílicos?', 520);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4911, '¿Qué tipo de enlace presentan los alquinos?', 520);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4956, '¿Cuál es la fórmula general para resolver ecuaciones cuadráticas?', 526);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4957, '¿Cuántas soluciones tiene una ecuación cuadrática con discriminante positivo?', 526);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4958, '¿Qué indica el discriminante en una ecuación cuadrática?', 526);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4959, 'Resuelve: x² - 5x + 6 = 0', 526);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4960, '¿Qué forma tiene la gráfica de una función cuadrática?', 526);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4961, '¿Cuál es el vértice de la parábola f(x) = x² - 4x + 3?', 526);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4962, '¿Qué método se usa para factorizar x² + 5x + 6?', 526);
INSERT INTO public.questions (id, question_text, test_id) VALUES (4963, 'Si el discriminante es 0, ¿cómo son las soluciones?', 526);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5004, '¿Qué es AWS?', 532);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5005, '¿Qué servicio de AWS ofrece almacenamiento de objetos escalable?', 532);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5006, '¿Qué significa EC2 en AWS?', 532);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5007, '¿Cuál es el modelo de pago en AWS?', 532);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5008, '¿Qué servicio gestiona bases de datos relacionales en AWS?', 532);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5009, '¿Qué es una región en AWS?', 532);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5010, '¿Qué servicio permite ejecutar código sin gestionar servidores?', 532);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5011, '¿Qué es un balanceador de carga en AWS?', 532);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5047, '¿Cuál fue el nombre del plan alemán para invadir la Unión Soviética en 1941?', 538);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5048, '¿Quién fue el líder de la Unión Soviética durante la Segunda Guerra Mundial?', 538);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5049, '¿En qué año se llevó a cabo la Conferencia de Yalta?', 538);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5050, '¿Cuál fue el nombre del campo de concentración nazi en Polonia donde se estima que murieron más de un millón de personas?', 538);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5051, '¿Quién fue el primer ministro del Reino Unido durante la mayor parte de la Segunda Guerra Mundial?', 538);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5052, '¿Cuál fue el nombre del bombardero alemán utilizado durante la Batalla de Inglaterra?', 538);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5053, '¿En qué ciudad se llevó a cabo la rendición incondicional de Alemania en 1945?', 538);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5054, '¿Quién fue el líder de la resistencia francesa durante la Segunda Guerra Mundial?', 538);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5055, '¿Cuál fue el nombre del programa de préstamos y arrendamientos implementado por Estados Unidos para ayudar a sus aliados durante la Segunda Guerra Mundial?', 538);
INSERT INTO public.questions (id, question_text, test_id) VALUES (5056, '¿En qué fecha comenzó la Segunda Guerra Mundial?', 538);


--
-- Data for Name: answers; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18645, 'F = ma', false, 4877);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18646, 'Todo cuerpo mantiene su estado de reposo o movimiento uniforme a menos que una fuerza externa actúe sobre él', true, 4877);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18647, 'A toda acción hay una reacción igual y opuesta', false, 4877);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18648, 'La aceleración es inversamente proporcional a la masa', false, 4877);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18649, 'F = m * a', true, 4878);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18650, 'F = m / a', false, 4878);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18651, 'F = a / m', false, 4878);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18652, 'F = m + a', false, 4878);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18653, 'Fuerza normal', false, 4879);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18654, 'Fuerza de fricción', true, 4879);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18655, 'Fuerza centrípeta', false, 4879);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18656, 'Fuerza gravitacional', false, 4879);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18657, 'La capacidad de un cuerpo para cambiar de forma', false, 4880);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18658, 'La tendencia de un cuerpo a mantener su estado de movimiento', true, 4880);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18659, 'La fuerza necesaria para acelerar un cuerpo', false, 4880);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18660, 'La velocidad máxima que puede alcanzar un cuerpo', false, 4880);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18661, '2 m/s²', false, 4881);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18662, '5 m/s²', true, 4881);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18663, '10 m/s²', false, 4881);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18664, '0.5 m/s²', false, 4881);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18665, 'Newton', true, 4882);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18666, 'Joule', false, 4882);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18667, 'Pascal', false, 4882);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18668, 'Watt', false, 4882);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18669, 'La energía se conserva en todo sistema', false, 4883);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18670, 'A toda acción le corresponde una reacción igual y opuesta', true, 4883);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18671, 'La aceleración es directamente proporcional a la masa', false, 4883);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18672, 'La velocidad es constante en ausencia de fuerzas', false, 4883);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18673, 'Movimiento circular uniforme', false, 4884);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18674, 'Movimiento rectilíneo uniformemente acelerado', true, 4884);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18675, 'Movimiento armónico simple', false, 4884);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18676, 'Movimiento parabólico', false, 4884);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18677, '49 N', true, 4885);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18678, '5 N', false, 4885);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18679, '9.8 N', false, 4885);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18680, '98 N', false, 4885);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18569, 'x = 5', true, 4858);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18570, 'x = 7', false, 4858);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18571, 'x = 3', false, 4858);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18572, 'x = 9', false, 4858);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18573, 'Encontrar los valores de las variables que cumplen la igualdad', true, 4859);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18574, 'Simplificar la expresión a su forma más básica', false, 4859);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18575, 'Factorizar todos los términos', false, 4859);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18576, 'Graficar la función en un plano cartesiano', false, 4859);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18577, 'y = mx + b', false, 4860);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18578, 'ax + b = 0', true, 4860);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18579, 'ax² + bx + c = 0', false, 4860);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18580, 'y = ax² + bx + c', false, 4860);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18581, 'x = 7', true, 4861);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18582, 'x = 5', false, 4861);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18583, 'x = 6', false, 4861);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18584, 'x = 4', false, 4861);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18585, 'Propiedad de la multiplicación por cero', false, 4862);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18586, 'Propiedad de la división', true, 4862);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18587, 'Propiedad conmutativa', false, 4862);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18588, 'Propiedad distributiva', false, 4862);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18589, 'Una solución', true, 4863);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18590, 'Dos soluciones', false, 4863);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18591, 'Infinitas soluciones', false, 4863);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18592, 'Ninguna solución', false, 4863);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18593, 'x = 25', false, 4864);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18594, 'x = 16', false, 4864);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18595, 'x = 12', false, 4864);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18596, 'x = 20', true, 4864);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18597, 'Sumar 5 en ambos lados', false, 4865);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18598, 'Restar 5 en ambos lados', true, 4865);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18599, 'Multiplicar por 5 ambos lados', false, 4865);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18600, 'Dividir entre 5 ambos lados', false, 4865);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18601, 'x = 7', true, 4866);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18602, 'x = 8', false, 4866);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18603, 'x = 6', false, 4866);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18604, 'x = 5', false, 4866);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18717, 'Julio César', false, 4895);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18718, 'Augusto', true, 4895);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18719, 'Nerón', false, 4895);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18720, 'Trajano', false, 4895);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18721, '476 d.C.', true, 4896);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18722, '410 d.C.', false, 4896);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18723, '500 d.C.', false, 4896);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18724, '336 d.C.', false, 4896);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18725, 'Griego', false, 4897);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18726, 'Latín', true, 4897);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18727, 'Italiano', false, 4897);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18728, 'Francés', false, 4897);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18729, 'El Partenón', false, 4898);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18730, 'El Coliseo', true, 4898);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18731, 'La Torre Eiffel', false, 4898);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18732, 'El Panteón', false, 4898);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18733, 'Pompeyo', false, 4899);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18734, 'Julio César', true, 4899);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18735, 'Marco Antonio', false, 4899);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18736, 'Cicerón', false, 4899);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18737, 'Vías Appias', false, 4900);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18738, 'Calzadas romanas', true, 4900);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18739, 'Autovías', false, 4900);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18740, 'Carreteras', false, 4900);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18741, 'Cristianismo', true, 4901);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18742, 'Islam', false, 4901);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18743, 'Judaísmo', false, 4901);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18744, 'Budismo', false, 4901);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18745, 'Curia', false, 4902);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18746, 'Senatus', true, 4902);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18747, 'Asamblea', false, 4902);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18748, 'Concilio', false, 4902);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18785, 'Rendirse', true, 4912);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18786, 'Dar algo', false, 4912);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18787, 'Levantarse', false, 4912);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18788, 'Entregar', false, 4912);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18789, 'Go on', true, 4913);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18790, 'Go out', false, 4913);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18791, 'Go away', false, 4913);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18792, 'Go over', false, 4913);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18793, 'Mirar atrás', false, 4914);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18794, 'Cuidar', true, 4914);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18795, 'Buscar', false, 4914);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18796, 'Observar', false, 4914);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18797, 'Put on', false, 4915);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18798, 'Put off', true, 4915);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18799, 'Put up', false, 4915);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18800, 'Put out', false, 4915);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18801, 'Descomponerse, fallar', true, 4916);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18802, 'Romper algo', false, 4916);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18803, 'Entrar', false, 4916);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18605, '// comentario', false, 4867);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18606, '# comentario', true, 4867);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18607, '/* comentario */', false, 4867);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18608, '-- comentario', false, 4867);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18609, '6', false, 4868);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18610, '8', true, 4868);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18611, '9', false, 4868);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18612, '5', false, 4868);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18613, 'String', false, 4869);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18614, 'Booleano', true, 4869);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18615, 'Entero', false, 4869);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18616, 'Flotante', false, 4869);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18617, 'array = {1, 2, 3}', false, 4870);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18618, 'lista = [1, 2, 3]', true, 4870);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18619, 'lista = (1, 2, 3)', false, 4870);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18620, 'lista = <1, 2, 3>', false, 4870);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18621, 'float()', false, 4871);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18622, 'int()', true, 4871);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18623, 'str()', false, 4871);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18624, 'bool()', false, 4871);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18625, 'x > y', true, 4872);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18626, 'x >> y', false, 4872);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18627, 'x < y', false, 4872);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18628, 'x = y', false, 4872);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18629, '+', true, 4873);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18630, '.', false, 4873);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18631, '&', false, 4873);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18632, ',', false, 4873);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18633, '11', false, 4874);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18634, '10', true, 4874);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18635, '9', false, 4874);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18636, '12', false, 4874);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18637, 'int x = 5', false, 4875);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18638, 'x = 5', true, 4875);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18639, 'var x = 5', false, 4875);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18640, 'let x = 5', false, 4875);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18641, 'while', false, 4876);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18642, 'for', true, 4876);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18643, 'do-while', false, 4876);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18644, 'loop', false, 4876);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18681, 'getElementByClass()', false, 4886);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18682, 'getElementById()', true, 4886);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18683, 'getElementByTag()', false, 4886);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18684, 'querySelectorAll()', false, 4886);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18685, 'element.textContent = ''nuevo texto''', true, 4887);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18686, 'element.innerText = ''nuevo texto''', false, 4887);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18687, 'element.innerHTML = ''nuevo texto''', false, 4887);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18688, 'element.value = ''nuevo texto''', false, 4887);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18689, 'document.createElement()', true, 4888);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18690, 'document.newElement()', false, 4888);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18691, 'document.createNode()', false, 4888);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18692, 'document.addElement()', false, 4888);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18693, 'element.onClick = function() {}', false, 4889);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18694, 'element.addEventListener(''click'', function() {})', true, 4889);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18695, 'element.click(function() {})', false, 4889);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18696, 'element.setEvent(''click'', function() {})', false, 4889);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18697, 'element.innerHTML', false, 4890);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18698, 'element.value', true, 4890);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18699, 'element.textContent', false, 4890);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18700, 'element.innerText', false, 4890);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18701, 'document.getElementsByClass()', false, 4891);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18702, 'document.querySelectorAll(''.clase'')', true, 4891);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18703, 'document.getElementsByName()', false, 4891);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18704, 'document.getElementsByClassName()', false, 4891);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18705, 'element.delete()', false, 4892);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18706, 'element.remove()', true, 4892);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18707, 'element.erase()', false, 4892);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18708, 'element.hide()', false, 4892);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18709, 'element.class = ''nuevaClase''', false, 4893);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18710, 'element.classList.add(''nuevaClase'')', true, 4893);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18711, 'element.addClass(''nuevaClase'')', false, 4893);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18712, 'element.style.class = ''nuevaClase''', false, 4893);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18713, 'global', false, 4894);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18714, 'window', true, 4894);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18715, 'document', false, 4894);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18716, 'navigator', false, 4894);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18749, 'Carbonilo', false, 4903);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18750, 'Hidroxilo (-OH)', true, 4903);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18751, 'Carboxilo', false, 4903);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18752, 'Amino', false, 4903);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18753, 'C6H12O6', true, 4904);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18754, 'C12H22O11', false, 4904);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18755, 'C5H10O5', false, 4904);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18756, 'C3H6O3', false, 4904);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18757, 'Eliminación', false, 4905);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18758, 'Hidrogenación', true, 4905);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18759, 'Oxidación', false, 4905);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18760, 'Sustitución', false, 4905);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18761, 'Butano', true, 4906);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18762, 'Propano', false, 4906);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18763, 'Pentano', false, 4906);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18764, 'Hexano', false, 4906);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18765, '-OH', false, 4907);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18766, '-COOH', true, 4907);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18767, '-NH2', false, 4907);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18768, '-COH', false, 4907);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18769, 'Compuesto con dobles enlaces conjugados en un anillo', true, 4908);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18770, 'Compuesto con enlaces simples', false, 4908);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18771, 'Compuesto con triple enlace', false, 4908);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18772, 'Compuesto con oxígeno', false, 4908);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18773, 'C6H6', true, 4909);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18774, 'C6H12', false, 4909);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18775, 'C6H10', false, 4909);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18776, 'C8H10', false, 4909);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18777, 'Adición nucleofílica', true, 4910);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18778, 'Eliminación', false, 4910);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18779, 'Sustitución', false, 4910);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18780, 'Oxidación', false, 4910);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18781, 'Enlace simple', false, 4911);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18782, 'Enlace doble', false, 4911);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18783, 'Enlace triple', true, 4911);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18784, 'Enlace iónico', false, 4911);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18804, 'Salir corriendo', false, 4916);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18805, 'Find out', true, 4917);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18806, 'Look up', false, 4917);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18807, 'Figure out', false, 4917);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18808, 'Check out', false, 4917);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18809, 'Quitarse ropa o despegar', true, 4918);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18810, 'Tomar algo', false, 4918);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18811, 'Apagar', false, 4918);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18812, 'Encender', false, 4918);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18813, 'Look forward to', true, 4919);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18814, 'Look for', false, 4919);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18815, 'Look at', false, 4919);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18816, 'Look into', false, 4919);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18817, 'Una estimación de ingresos y gastos en un periodo', true, 4920);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18818, 'Un préstamo bancario', false, 4920);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18819, 'Una cuenta de ahorro', false, 4920);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18820, 'Una tarjeta de crédito', false, 4920);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18821, '50% necesidades, 30% deseos, 20% ahorro', true, 4921);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18822, '50% ahorro, 30% inversión, 20% gastos', false, 4921);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18823, '50% deseos, 30% necesidades, 20% ahorro', false, 4921);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18824, '50% gastos, 30% ahorro, 20% deudas', false, 4921);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18825, 'El fijo cambia mensualmente', false, 4922);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18826, 'El fijo es constante y el variable fluctúa', true, 4922);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18827, 'El variable es más importante', false, 4922);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18828, 'No hay diferencia', false, 4922);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18829, 'Al menos 10%', false, 4923);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18830, 'Al menos 20%', true, 4923);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18831, 'Al menos 30%', false, 4923);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18832, 'Al menos 5%', false, 4923);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18833, 'Dinero guardado para gastos inesperados', true, 4924);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18834, 'Una tarjeta de crédito', false, 4924);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18835, 'Un préstamo personal', false, 4924);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18836, 'Un seguro de vida', false, 4924);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18837, 'Aplicaciones de finanzas personales', true, 4925);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18838, 'Tarjeta de débito', false, 4925);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18839, 'Chequera', false, 4925);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18840, 'Efectivo', false, 4925);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18841, 'Dinero que se gana sin trabajo activo', true, 4926);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18842, 'Salario mensual', false, 4926);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18843, 'Propinas', false, 4926);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18844, 'Bonos del trabajo', false, 4926);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18845, '1-2 meses', false, 4927);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18846, '3-6 meses', true, 4927);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18847, '12 meses', false, 4927);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18848, '1 mes', false, 4927);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18849, 'Dos', false, 4928);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18850, 'Tres', true, 4928);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18851, 'Cuatro', false, 4928);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18852, 'Cinco', false, 4928);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18853, 'Tónica, tercera mayor, quinta justa', true, 4929);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18854, 'Tónica, tercera menor, quinta justa', false, 4929);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18855, 'Tónica, cuarta, quinta', false, 4929);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18856, 'Tónica, segunda, quinta', false, 4929);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18857, 'La menor', true, 4930);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18858, 'Mi menor', false, 4930);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18859, 'Sol menor', false, 4930);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18860, 'Fa menor', false, 4930);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18861, 'Se añade una séptima nota a la tríada', true, 4931);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18862, 'Se toca siete veces', false, 4931);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18863, 'Se cambia la tónica', false, 4931);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18864, 'Se invierte el acorde', false, 4931);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18865, 'C7', true, 4932);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18866, 'Cmaj7', false, 4932);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18867, 'Cm7', false, 4932);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18868, 'Cdim7', false, 4932);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18869, 'Cambiar el orden de las notas del acorde', true, 4933);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18870, 'Cambiar la tonalidad', false, 4933);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18871, 'Añadir más notas', false, 4933);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18872, 'Tocar más rápido', false, 4933);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18873, 'Dos', false, 4934);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18874, 'Tres', true, 4934);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18875, 'Cuatro', false, 4934);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18876, 'Una', false, 4934);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18877, 'Acorde menor', true, 4935);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18878, 'Acorde mayor', false, 4935);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18879, 'Acorde disminuido', false, 4935);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18880, 'Acorde aumentado', false, 4935);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18921, '15 minutos', false, 4946);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18922, '20 minutos', false, 4946);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18923, '25 minutos', true, 4946);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18924, '30 minutos', false, 4946);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18925, '3 minutos', false, 4947);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18926, '5 minutos', true, 4947);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18927, '10 minutos', false, 4947);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18928, '15 minutos', false, 4947);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18929, '3', false, 4948);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18930, '4', true, 4948);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18931, '5', false, 4948);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18932, '6', false, 4948);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18933, 'Trabajar más horas', false, 4949);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18934, 'Mejorar la concentración y productividad', true, 4949);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18935, 'Dormir mejor', false, 4949);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18936, 'Aprender más rápido', false, 4949);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18937, 'Un calendario', false, 4950);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18938, 'Un temporizador', true, 4950);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18939, 'Una lista de compras', false, 4950);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18940, 'Un reloj de pulsera', false, 4950);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18941, 'Ignorar la interrupción', false, 4951);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18942, 'Anotar la interrupción y continuar', true, 4951);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18943, 'Reiniciar el Pomodoro', false, 4951);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18944, 'Cancelar la sesión', false, 4951);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18945, '10-15 minutos', false, 4952);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18946, '15-30 minutos', true, 4952);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18947, '30-45 minutos', false, 4952);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18948, '5-10 minutos', false, 4952);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18949, 'Francesco Cirillo', true, 4953);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18950, 'Steve Jobs', false, 4953);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18951, 'Albert Einstein', false, 4953);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18952, 'Marie Curie', false, 4953);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18953, 'Tomate en italiano', true, 4954);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18954, 'Tiempo en japonés', false, 4954);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18955, 'Reloj en latín', false, 4954);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18956, 'Pausa en francés', false, 4954);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18957, 'Revisar el correo', false, 4955);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18958, 'Estirarse o caminar', true, 4955);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18959, 'Continuar trabajando', false, 4955);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18960, 'Hacer más tareas', false, 4955);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18881, 'Un sistema que monitorea y controla el tráfico de red', true, 4936);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18882, 'Un virus informático', false, 4936);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18883, 'Un tipo de servidor', false, 4936);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18884, 'Un cable de red', false, 4936);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18885, 'HTTPS', true, 4937);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18886, 'HTTP', false, 4937);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18887, 'FTP', false, 4937);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18888, 'SMTP', false, 4937);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18889, 'DDoS', true, 4938);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18890, 'Phishing', false, 4938);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18891, 'Man-in-the-middle', false, 4938);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18892, 'SQL Injection', false, 4938);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18893, 'Autenticar y cifrar la comunicación', true, 4939);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18894, 'Acelerar la conexión', false, 4939);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18895, 'Comprimir datos', false, 4939);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18896, 'Almacenar contraseñas', false, 4939);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18897, 'Una red local virtual que segmenta el tráfico', true, 4940);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18898, 'Un tipo de cable de red', false, 4940);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18899, 'Un protocolo de enrutamiento', false, 4940);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18900, 'Un sistema operativo', false, 4940);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18901, 'Phishing', true, 4941);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18902, 'Brute force', false, 4941);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18903, 'Man-in-the-middle', false, 4941);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18904, 'DDoS', false, 4941);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18905, 'Una red privada virtual que cifra la comunicación', true, 4942);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18906, 'Un protocolo de correo', false, 4942);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18907, 'Un tipo de servidor web', false, 4942);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18908, 'Un firewall', false, 4942);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18909, '443', true, 4943);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18910, '80', false, 4943);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18911, '21', false, 4943);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18912, '22', false, 4943);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18913, '2FA', true, 4944);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18914, 'SSO', false, 4944);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18915, 'OAuth', false, 4944);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18916, 'LDAP', false, 4944);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18917, 'Sistema de detección de intrusiones', true, 4945);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18918, 'Sistema de prevención de intrusiones', false, 4945);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18919, 'Sistema de gestión de identidades', false, 4945);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18920, 'Sistema de monitoreo de red', false, 4945);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18961, 'x = (-b ± √(b² - 4ac)) / 2a', true, 4956);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18962, 'x = (b ± √(b² + 4ac)) / 2a', false, 4956);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18963, 'x = (-b ± √(b² - 4ac)) / a', false, 4956);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18964, 'Dos soluciones reales', true, 4957);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18965, 'Una solución real', false, 4957);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18966, 'Ninguna solución real', false, 4957);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18967, 'El número y tipo de soluciones', true, 4958);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18968, 'El valor de la variable', false, 4958);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18969, 'El vértice de la parábola', false, 4958);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18970, 'x = 2, x = 3', true, 4959);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18971, 'x = 1, x = 6', false, 4959);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18972, 'x = -2, x = -3', false, 4959);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18973, 'Parábola', true, 4960);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18974, 'Línea recta', false, 4960);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18975, 'Elipse', false, 4960);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18976, '(2, -1)', true, 4961);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18977, '(-2, -1)', false, 4961);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18978, '(2, 1)', false, 4961);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18979, 'Buscar dos números que sumen 5 y multipliquen 6', true, 4962);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18980, 'Buscar dos números que sumen 6 y multipliquen 5', false, 4962);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18981, 'Aplicar la fórmula cuadrática', false, 4962);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18982, 'Dos soluciones iguales', true, 4963);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18983, 'Dos soluciones diferentes', false, 4963);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18984, 'No hay soluciones reales', false, 4963);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18985, 'def nombre_funcion():', true, 4964);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18986, 'function nombre_funcion():', false, 4964);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18987, 'fun nombre_funcion():', false, 4964);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18988, 'return', true, 4965);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18989, 'result', false, 4965);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18990, 'output', false, 4965);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18991, 'Valores que recibe la función', true, 4966);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18992, 'Lo que devuelve la función', false, 4966);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18993, 'Variables globales', false, 4966);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18994, '6', true, 4967);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18995, '5', false, 4967);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18996, '7', false, 4967);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18997, 'Genera números del 0 al 4', true, 4968);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18998, 'Genera números del 1 al 5', false, 4968);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (18999, 'Genera números del 0 al 5', false, 4968);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19000, 'El contexto donde la variable es accesible', true, 4969);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19001, 'El tipo de dato de la variable', false, 4969);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19002, 'El valor que almacena', false, 4969);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19003, 'Una función que se llama a sí misma', true, 4970);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19004, 'Una función que llama a otra función', false, 4970);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19005, 'Una función sin parámetros', false, 4970);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19006, 'None', true, 4971);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19007, '0', false, 4971);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19008, 'Error', false, 4971);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19009, 'La pendiente de la recta tangente', true, 4972);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19010, 'El área bajo la curva', false, 4972);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19011, 'El valor máximo de la función', false, 4972);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19012, 'f''(x) = 3x²', true, 4973);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19013, 'f''(x) = 3x³', false, 4973);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19014, 'f''(x) = x²', false, 4973);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19015, 'Regla del producto', true, 4974);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19016, 'Regla de la cadena', false, 4974);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19017, 'Regla del cociente', false, 4974);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19018, 'f''(x) = cos(x)', true, 4975);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19019, 'f''(x) = -cos(x)', false, 4975);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19020, 'f''(x) = tan(x)', false, 4975);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19021, 'Donde la derivada es cero o no existe', true, 4976);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19022, 'Donde la función se hace cero', false, 4976);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19023, 'Donde la función es continua', false, 4976);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19024, 'f''(x) = eˣ', true, 4977);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19025, 'f''(x) = x·eˣ', false, 4977);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19026, 'f''(x) = e', false, 4977);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19027, 'Teorema del valor medio', true, 4978);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19028, 'Teorema fundamental del cálculo', false, 4978);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19029, 'Teorema de Rolle', false, 4978);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19030, 'f''''(x) = 12x²', true, 4979);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19031, 'f''''(x) = 4x³', false, 4979);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19032, 'f''''(x) = 12x', false, 4979);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19033, '1789', true, 4980);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19034, '1776', false, 4980);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19035, '1799', false, 4980);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19036, 'La Toma de la Bastilla', true, 4981);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19037, 'La ejecución de Luis XVI', false, 4981);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19038, 'El Manifiesto de los Derechos', false, 4981);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19039, 'Libertad, Igualdad, Fraternidad', true, 4982);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19040, 'Paz, Amor, Unión', false, 4982);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19041, 'Justicia, Verdad, Honor', false, 4982);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19042, 'Luis XVI y María Antonieta', true, 4983);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19043, 'Napoleón Bonaparte', false, 4983);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19044, 'Robespierre', false, 4983);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19045, '1793-1794', true, 4984);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19046, '1789-1790', false, 4984);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19047, '1795-1796', false, 4984);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19048, 'Robespierre', true, 4985);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19049, 'Danton', false, 4985);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19050, 'Marat', false, 4985);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19051, 'Declaración de los Derechos del Hombre', true, 4986);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19052, 'Constitución de 1791', false, 4986);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19053, 'Código Napoleónico', false, 4986);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19054, 'El Directorio', true, 4987);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19055, 'El Imperio Napoleónico', false, 4987);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19056, 'La Monarquía Constitucional', false, 4987);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19057, 'Una secuencia de ADN que codifica una proteína', true, 4988);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19058, 'Una proteína en el núcleo celular', false, 4988);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19059, 'Un cromosoma completo', false, 4988);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19060, '46', true, 4989);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19061, '44', false, 4989);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19062, '48', false, 4989);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19063, 'El material genético que contiene la información hereditaria', true, 4990);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19064, 'Una proteína estructural', false, 4990);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19065, 'Un tipo de célula', false, 4990);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19066, 'Ley de la segregación independiente', true, 4991);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19067, 'Ley de la dominancia', false, 4991);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19068, 'Ley de la herencia ligada', false, 4991);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19069, 'Meiosis', true, 4992);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19070, 'Mitosis', false, 4992);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19071, 'Fisión', false, 4992);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19072, 'Una variante de un gen', true, 4993);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19073, 'Un cromosoma entero', false, 4993);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19074, 'Una mutación en el ADN', false, 4993);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19075, 'El genotipo es la composición genética, el fenotipo la expresión observable', true, 4994);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19076, 'El fenotipo es genético y el genotipo es ambiental', false, 4994);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19077, 'Son sinónimos', false, 4994);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19078, 'El núcleo', true, 4995);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19079, 'La membrana celular', false, 4995);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19080, 'El citoplasma', false, 4995);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19081, 'Do, Re, Mi, Fa, Sol, La, Si', true, 4996);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19082, 'Do, Fa, Sol', false, 4996);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19083, 'Do mayor, La menor, Mi menor', false, 4996);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19084, 'Con tónica, tercera mayor y quinta justa', true, 4997);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19085, 'Con tónica, tercera menor y quinta justa', false, 4997);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19086, 'Con tónica y quinta', false, 4997);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19087, 'Índice', true, 4998);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19088, 'Medio', false, 4998);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19089, 'Anular', false, 4998);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19090, 'Presionar varias cuerdas con un solo dedo', true, 4999);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19091, 'Tocar una sola cuerda', false, 4999);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19092, 'Afinar la guitarra', false, 4999);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19093, 'Mi menor', true, 5000);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19094, 'Do mayor', false, 5000);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19095, 'Sol mayor', false, 5000);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19096, 'La tercera es mayor o menor', true, 5001);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19097, 'La tónica cambia', false, 5001);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19098, 'La quinta es diferente', false, 5001);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19099, '6', true, 5002);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19100, '4', false, 5002);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19101, '7', false, 5002);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19102, 'Do mayor', true, 5003);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19103, 'Sol mayor', false, 5003);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19104, 'La mayor', false, 5003);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19105, 'Amazon Web Services, plataforma de servicios en la nube', true, 5004);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19106, 'Advanced Web Security', false, 5004);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19107, 'Automatic Work System', false, 5004);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19108, 'S3', true, 5005);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19109, 'EC2', false, 5005);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19110, 'RDS', false, 5005);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19111, 'Elastic Compute Cloud', true, 5006);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19112, 'Elastic Container Cloud', false, 5006);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19113, 'Efficient Computing Cloud', false, 5006);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19114, 'Pago por uso', true, 5007);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19115, 'Suscripción anual fija', false, 5007);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19116, 'Gratuito completamente', false, 5007);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19117, 'RDS', true, 5008);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19118, 'DynamoDB', false, 5008);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19119, 'Redshift', false, 5008);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19120, 'Una ubicación geográfica con centros de datos', true, 5009);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19121, 'Un tipo de instancia', false, 5009);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19122, 'Un servicio de seguridad', false, 5009);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19123, 'Lambda', true, 5010);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19124, 'EC2', false, 5010);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19125, 'Beanstalk', false, 5010);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19126, 'Un servicio que distribuye tráfico entre instancias', true, 5011);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19127, 'Un servicio de almacenamiento', false, 5011);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19128, 'Un tipo de base de datos', false, 5011);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19129, 'El aumento generalizado y sostenido de los precios', true, 5012);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19130, 'La disminución del poder adquisitivo', false, 5012);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19131, 'El aumento del desempleo', false, 5012);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19132, 'Índice de Precios al Consumidor (IPC)', true, 5013);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19133, 'Producto Interno Bruto (PIB)', false, 5013);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19134, 'Índice de Desarrollo Humano', false, 5013);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19135, 'Aumento de la demanda agregada', true, 5014);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19136, 'Disminución de la oferta monetaria', false, 5014);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19137, 'Reducción de los salarios', false, 5014);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19138, 'Inflación extremadamente alta y acelerada', true, 5015);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19139, 'Inflación negativa', false, 5015);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19140, 'Inflación moderada del 2%', false, 5015);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19141, 'Reduce el poder adquisitivo de los ahorros', true, 5016);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19142, 'Aumenta el valor de los ahorros', false, 5016);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19143, 'No tiene ningún efecto', false, 5016);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19144, 'El banco central', true, 5017);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19145, 'El ministerio de educación', false, 5017);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19146, 'El ministerio de transporte', false, 5017);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19147, 'La caída generalizada de los precios', true, 5018);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19148, 'El aumento de precios controlado', false, 5018);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19149, 'La estabilidad de precios', false, 5018);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19150, 'Tasas de interés', true, 5019);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19151, 'Impuestos sobre la renta', false, 5019);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19152, 'Subsidios a empresas', false, 5019);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19153, 'Practicar y conocer bien el tema', true, 5020);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19154, 'Memorizar todo el discurso', false, 5020);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19155, 'Hablar lo más rápido posible', false, 5020);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19156, 'Es fundamental para transmitir confianza y mensaje', true, 5021);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19157, 'No tiene importancia, solo importa lo que se dice', false, 5021);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19158, 'Solo importa al inicio', false, 5021);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19159, 'Respirar profundamente y visualizar el éxito', true, 5022);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19160, 'Beber café para estar más activo', false, 5022);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19161, 'Evitar mirar al público', false, 5022);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19162, 'Introducción, desarrollo y conclusión', true, 5023);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19163, 'Inicio, medio y despedida', false, 5023);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19164, 'Resumen, detalles y cierre', false, 5023);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19165, 'Aceptarlos y usarlos como energía positiva', true, 5024);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19166, 'Eliminarlos completamente', false, 5024);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19167, 'Ignorarlos', false, 5024);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19168, 'Depende del tema y la audiencia', true, 5025);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19169, 'Siempre 30 minutos', false, 5025);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19170, 'Máximo 5 minutos', false, 5025);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19171, 'Permiten enfatizar y que el público asimile la información', true, 5026);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19172, 'Solo sirven para respirar', false, 5026);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19173, 'Demuestran inseguridad', false, 5026);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19174, 'Claro, audible y con variaciones para mantener el interés', true, 5027);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19175, 'Monótono para ser profesional', false, 5027);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19176, 'Muy alto todo el tiempo', false, 5027);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19177, 'Un contrato autoejecutable con código en blockchain', true, 5028);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19178, 'Un contrato legal en papel', false, 5028);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19179, 'Un tipo de criptomoneda', false, 5028);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19180, 'Ethereum', true, 5029);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19181, 'Bitcoin', false, 5029);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19182, 'Ripple', false, 5029);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19183, 'Solidity', true, 5030);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19184, 'JavaScript', false, 5030);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19185, 'Python', false, 5030);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19186, 'Transparencia y ejecución automática sin intermediarios', true, 5031);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19187, 'Reducción de costos legales', false, 5031);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19188, 'Mayor velocidad de ejecución', false, 5031);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19189, 'Aplicación descentralizada que usa smart contracts', true, 5032);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19190, 'Una aplicación de escritorio tradicional', false, 5032);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19191, 'Un tipo de antivirus', false, 5032);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19192, 'La necesidad de confianza en transacciones', true, 5033);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19193, 'El almacenamiento de datos', false, 5033);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19194, 'La velocidad de internet', false, 5033);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19195, 'La tarifa pagada para ejecutar smart contracts', true, 5034);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19196, 'Un tipo de token', false, 5034);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19197, 'El combustible del sistema', false, 5034);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19198, 'No, son inmutables en la mayoría de casos', true, 5035);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19199, 'Sí, se pueden modificar libremente', false, 5035);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19200, 'Solo si se aprueba una votación', false, 5035);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19234, 'Operación Barbarroja', true, 5047);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19235, 'Operación Overlord', false, 5047);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19236, 'Operación Sea Lion', false, 5047);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19237, 'Iósif Stalin', true, 5048);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19238, 'Lavrenti Beria', false, 5048);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19239, 'Viacheslav Molotov', false, 5048);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19240, '1945', true, 5049);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19241, '1943', false, 5049);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19242, '1942', false, 5049);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19243, 'Auschwitz-Birkenau', true, 5050);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19244, 'Treblinka', false, 5050);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19245, 'Buchenwald', false, 5050);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19246, 'Winston Churchill', true, 5051);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19247, 'Neville Chamberlain', false, 5051);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19248, 'Clement Attlee', false, 5051);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19249, 'Junkers Ju 87', false, 5052);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19250, 'Messerschmitt Bf 109', false, 5052);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19251, 'Heinkel He 111', true, 5052);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19252, 'Berlín', true, 5053);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19253, 'París', false, 5053);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19254, 'Moscú', false, 5053);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19255, 'Charles de Gaulle', true, 5054);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19256, 'Jean Moulin', false, 5054);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19257, 'Philippe Pétain', false, 5054);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19258, 'Ley de Préstamos y Arrendamientos', true, 5055);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19259, 'Plan Marshall', false, 5055);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19260, 'Acuerdo de Ayuda Mutua', false, 5055);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19261, '1 de septiembre de 1939', true, 5056);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19262, '3 de septiembre de 1939', false, 5056);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19263, '15 de agosto de 1939', false, 5056);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19264, 'Recoger o tomar algo', true, 5057);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19265, 'Dejar caer algo', false, 5057);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19266, 'Comprar algo', false, 5057);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19267, 'Subir a un vehículo', true, 5058);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19268, 'Bajar de un vehículo', false, 5058);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19269, 'Conducir un vehículo', false, 5058);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19270, 'Apagar algo', true, 5059);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19271, 'Encender algo', false, 5059);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19272, 'Arreglar algo', false, 5059);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19273, 'Ponerse ropa o algo', true, 5060);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19274, 'Quitarse ropa o algo', false, 5060);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19275, 'Romper algo', false, 5060);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19276, 'Quitarse algo o despegar', true, 5061);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19277, 'Ponerse algo', false, 5061);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19278, 'Volar alto', false, 5061);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19279, 'Rendirse o abandonar', true, 5062);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19280, 'Continuar adelante', false, 5062);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19281, 'Olvidar algo', false, 5062);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19282, 'Cuidar de alguien o algo', true, 5063);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19283, 'Mirar algo fijamente', false, 5063);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19284, 'Olvidar algo', false, 5063);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19285, 'Continuar haciendo algo', true, 5064);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19286, 'Apagarse', false, 5064);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19287, 'Detenerse', false, 5064);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19288, 'Despertar', true, 5065);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19289, 'Dormir profundamente', false, 5065);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19290, 'Soñar', false, 5065);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19291, 'Criar o educar a alguien', true, 5066);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19292, 'Bajar algo', false, 5066);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19293, 'Olvidar algo', false, 5066);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19294, 'Maximizar las ganancias', false, 5067);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19295, 'Limitar las pérdidas', true, 5067);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19296, 'Incrementar el leverage', false, 5067);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19297, 'Análisis fundamental', false, 5068);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19298, 'Análisis técnico', true, 5068);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19299, 'Análisis cuantitativo', false, 5068);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19300, 'MACD', false, 5069);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19301, 'RSI', false, 5069);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19302, 'Momentum', true, 5069);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19303, 'Swing trading', false, 5070);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19304, 'Day trading', true, 5070);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19305, 'Position trading', false, 5070);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19306, 'Correlación positiva', false, 5071);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19307, 'Correlación negativa', true, 5071);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19308, 'Correlación neutra', false, 5071);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19309, 'Orden de mercado', false, 5072);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19310, 'Orden limitada', true, 5072);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19311, 'Orden stop', false, 5072);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19312, 'Bollinger Bands', false, 5073);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19313, 'Ichimoku Cloud', true, 5073);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19314, 'Stochastic Oscillator', false, 5073);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19315, 'Contrarian', false, 5074);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19316, 'Trend following', true, 5074);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19317, 'Range trading', false, 5074);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19318, 'Aversión a la pérdida', false, 5075);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19319, 'Tolerancia al riesgo', false, 5075);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19320, 'Aversión al riesgo', true, 5075);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19321, 'Análisis técnico', false, 5076);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19322, 'Análisis fundamental', true, 5076);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19323, 'Análisis cuantitativo', false, 5076);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19324, 'Martillo', false, 5077);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19325, 'Estrella fugaz', false, 5077);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19326, 'Tumba de toro', true, 5077);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19327, 'Day trading', false, 5078);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19328, 'Swing trading', false, 5078);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19329, 'Position trading', true, 5078);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19330, 'Leverage', false, 5079);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19331, 'Margen', false, 5079);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19332, 'Exposición', true, 5079);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19333, 'Media móvil', false, 5080);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19334, 'Bollinger Bands', true, 5080);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19335, 'RSI', false, 5080);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19336, 'Orden de mercado', false, 5081);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19337, 'Orden limitada', false, 5081);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19338, 'Orden stop', true, 5081);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19339, 'Liquidez', true, 5082);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19340, 'Volatilidad', false, 5082);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19341, 'Profundidad', false, 5082);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19342, 'Compraventa', false, 5083);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19343, 'Venta en corto', true, 5083);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19344, 'Cobertura', false, 5083);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19345, 'Tendencia', true, 5084);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19346, 'Reversión', false, 5084);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19347, 'Consolidación', false, 5084);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19348, 'Análisis fundamental', false, 5085);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19349, 'Análisis técnico', true, 5085);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19350, 'Análisis cuantitativo', false, 5085);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19351, 'Spread', true, 5086);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19352, 'Comisión', false, 5086);
INSERT INTO public.answers (id, answer_text, is_correct, question_id) VALUES (19353, 'Swap', false, 5086);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--



--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.django_content_type (id, app_label, model) VALUES (1, 'admin', 'logentry');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (2, 'auth', 'permission');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (3, 'auth', 'group');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (5, 'sessions', 'session');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (6, 'accounts', 'user');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (7, 'accounts', 'passwordresettoken');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (8, 'test', 'question');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (9, 'test', 'answer');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (10, 'test', 'test');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (11, 'results', 'result');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (12, 'admin_panel', 'systemconfig');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (13, 'admin_panel', 'userquota');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (14, 'invitations', 'testinvitation');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (15, 'invitations', 'invitationevent');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (16, 'shared', 'topic');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (17, 'ai', 'airequestlog');


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (21, 'Can add user', 6, 'add_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (22, 'Can change user', 6, 'change_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (23, 'Can delete user', 6, 'delete_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (24, 'Can view user', 6, 'view_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (25, 'Can add password reset token', 7, 'add_passwordresettoken');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (26, 'Can change password reset token', 7, 'change_passwordresettoken');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (27, 'Can delete password reset token', 7, 'delete_passwordresettoken');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (28, 'Can view password reset token', 7, 'view_passwordresettoken');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (29, 'Can add question', 8, 'add_question');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (30, 'Can change question', 8, 'change_question');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (31, 'Can delete question', 8, 'delete_question');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (32, 'Can view question', 8, 'view_question');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (33, 'Can add answer', 9, 'add_answer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (34, 'Can change answer', 9, 'change_answer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (35, 'Can delete answer', 9, 'delete_answer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (36, 'Can view answer', 9, 'view_answer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (37, 'Can add test', 10, 'add_test');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (38, 'Can change test', 10, 'change_test');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (39, 'Can delete test', 10, 'delete_test');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (40, 'Can view test', 10, 'view_test');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (41, 'Can add result', 11, 'add_result');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (42, 'Can change result', 11, 'change_result');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (43, 'Can delete result', 11, 'delete_result');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (44, 'Can view result', 11, 'view_result');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (45, 'Can add system config', 12, 'add_systemconfig');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (46, 'Can change system config', 12, 'change_systemconfig');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (47, 'Can delete system config', 12, 'delete_systemconfig');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (48, 'Can view system config', 12, 'view_systemconfig');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (49, 'Can add user quota', 13, 'add_userquota');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (50, 'Can change user quota', 13, 'change_userquota');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (51, 'Can delete user quota', 13, 'delete_userquota');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (52, 'Can view user quota', 13, 'view_userquota');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (53, 'Can add test invitation', 14, 'add_testinvitation');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (54, 'Can change test invitation', 14, 'change_testinvitation');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (55, 'Can delete test invitation', 14, 'delete_testinvitation');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (56, 'Can view test invitation', 14, 'view_testinvitation');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (57, 'Can add invitation event', 15, 'add_invitationevent');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (58, 'Can change invitation event', 15, 'change_invitationevent');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (59, 'Can delete invitation event', 15, 'delete_invitationevent');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (60, 'Can view invitation event', 15, 'view_invitationevent');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (61, 'Can add topic', 16, 'add_topic');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (62, 'Can change topic', 16, 'change_topic');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (63, 'Can delete topic', 16, 'delete_topic');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (64, 'Can view topic', 16, 'view_topic');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (65, 'Can add ai request log', 17, 'add_airequestlog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (66, 'Can change ai request log', 17, 'change_airequestlog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (67, 'Can delete ai request log', 17, 'delete_airequestlog');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (68, 'Can view ai request log', 17, 'view_airequestlog');


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--



--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--



--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.django_migrations (id, app, name, applied) VALUES (1, 'contenttypes', '0001_initial', '2026-06-11 14:37:19.727957+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2026-06-11 14:37:19.737044+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (3, 'auth', '0001_initial', '2026-06-11 14:37:19.819919+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2026-06-11 14:37:19.826412+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (5, 'auth', '0003_alter_user_email_max_length', '2026-06-11 14:37:19.833153+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (6, 'auth', '0004_alter_user_username_opts', '2026-06-11 14:37:19.839878+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (7, 'auth', '0005_alter_user_last_login_null', '2026-06-11 14:37:19.846881+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (8, 'auth', '0006_require_contenttypes_0002', '2026-06-11 14:37:19.850393+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2026-06-11 14:37:19.857044+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (10, 'auth', '0008_alter_user_username_max_length', '2026-06-11 14:37:19.864305+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2026-06-11 14:37:19.871921+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (12, 'auth', '0010_alter_group_name_max_length', '2026-06-11 14:37:19.880996+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (13, 'auth', '0011_update_proxy_permissions', '2026-06-11 14:37:19.889413+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2026-06-11 14:37:19.898437+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (15, 'accounts', '0001_initial', '2026-06-11 14:37:20.051066+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (16, 'admin', '0001_initial', '2026-06-11 14:37:20.09562+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (17, 'admin', '0002_logentry_remove_auto_add', '2026-06-11 14:37:20.104293+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (18, 'admin', '0003_logentry_add_action_flag_choices', '2026-06-11 14:37:20.114672+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (19, 'admin_panel', '0001_initial', '2026-06-11 14:37:20.218646+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (20, 'test', '0001_initial', '2026-06-11 14:37:20.339197+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (21, 'test', '0002_alter_test_created_by', '2026-06-11 14:37:20.352755+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (22, 'invitations', '0001_initial', '2026-06-11 14:37:20.538678+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (23, 'results', '0001_initial', '2026-06-11 14:37:20.604431+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (24, 'sessions', '0001_initial', '2026-06-11 14:37:20.63772+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (25, 'shared', '0001_initial', '2026-06-11 14:37:20.719434+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (26, 'accounts', '0002_add_optimization_indexes', '2026-06-15 18:22:06.755637+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (27, 'results', '0002_alter_result_started_at_alter_result_updated_at', '2026-06-16 18:06:13.421864+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (28, 'accounts', '0003_alter_user_registered_at', '2026-06-16 18:20:25.460185+00');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (29, 'ai', '0001_initial', '2026-06-16 20:05:23.625653+00');


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('w3cll9k42qykipsp9jmjr4r4utmvbbqm', '.eJxVjDEOwjAMRe-SGUUittOEkZ0zVE7skAJqpaadKu4OlTrA-t97fzM9r0vt16ZzP4i5GABz-h0T56eOO5EHj_fJ5mlc5iHZXbEHbfY2ib6uh_t3ULnVb108O0IMGGNwBNRhAUIoHaGSR5-yR4CQVcQxQ9HUedJzEiFPLhbz_gDdODeX:1wXvdd:z-YYRtupGx_xBANgLDzf5ggXOQ9UN0YDXQ-mJdzgq0Q', '2026-06-26 06:45:09.053998+00');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('b8n7urt05snnjr5jpkmfthahv932gaqd', '.eJxVjMsOwiAQRf-FtSG8AoxL934DGZhBqoYmpV0Z_12bdKHbe865L5FwW1vaBi9pInEWWoE4_a4Zy4P7juiO_TbLMvd1mbLcFXnQIa8z8fNyuH8HDUf71kZZMo7RVaUdWx1t8WRAqeCZgaoKObtSI0IErFQgO60tu-JD8BCteH8AJp44Fw:1wY1ff:EvCXEQP-z3-N3Jye6q8RVKtrEeQMR_gA7lkptJqWttY', '2026-06-26 13:11:39.351905+00');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('d9q17e4xwifdlbzv98nbnlafrubcrij2', '.eJxVjDsOwjAQBe_iGlm7mJiYkj5niPZnHECJFCcV4u4QKQW0b2bey_W0LqVfq839oO7iEMEdflcmedi4Ib3TeJu8TOMyD-w3xe-0-m5Se1539--gUC3fmqOFkFPOzAlbCqcGjxxRWg0CJAwNUgI9JyCkaMIhG0GCRhUUs7j3B0PHOTA:1wY2iE:KdS2w2SF6z8U55ZZMGaXjCgw3XAqAbDzRzCFkDBjDXE', '2026-06-26 14:18:22.350913+00');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('mi37m0vyzzlc0x3ptskcgtajvtefjaeg', '.eJxVjMsOwiAQRf-FtSGlPKa4dO83kIEZpGogKe3K-O_apAvd3nPOfYmA21rC1nkJM4mzUEqJ0-8aMT247ojuWG9NplbXZY5yV-RBu7w24uflcP8OCvbyrUH5CIOzaK1m8lonPyAYN7HXkE3EnBwgs6FxMhmZWIHzIznjko4M4v0BIeM4gg:1wY4Vf:knvaclhbINgboFjA-kNlUpmqu3esqDLcvlYnbxNUyVo', '2026-06-26 16:13:31.36426+00');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('6xeq8ttaw4antg5geapipe9wbgahm4pi', '.eJxVjMEOwiAQRP-FsyHLUil49O43EFgWqRpISnsy_rtt0oOeJpn3Zt7Ch3Upfu08-ymJi1AKxem3jYGeXHeUHqHem6RWl3mKclfkQbu8tcSv6-H-HZTQy7ZGS8BoIBCbHIZsECxjTFo7C8o6oi1QOz7TOChAg5Q5EkbQipUbxecLIK43wQ:1wY5hq:I_Fe1Q_tnhsqiCacFw1CedJKzpC4SzwzxwrDljztFMs', '2026-06-26 17:30:10.606594+00');


--
-- Data for Name: test_invitations; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--



--
-- Data for Name: invitation_events; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--



--
-- Data for Name: password_reset_tokens; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--



--
-- Data for Name: results; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (1996, 8, 0, 96, 'completed', '{"4928": 18850, "4929": 18853, "4930": 18857, "4931": 18861, "4932": 18865, "4933": 18869, "4934": 18874, "4935": 18877}', '2026-02-03 03:58:06+00', '2026-02-03 03:59:42+00', 523, 294);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (1997, 4, 4, 240, 'completed', '{"5004": 19106, "5005": 19109, "5006": 19112, "5007": 19114, "5008": 19117, "5009": 19120, "5010": 19124, "5011": 19126}', '2025-05-04 09:19:07.480531+00', '2025-05-04 09:23:07.480531+00', 532, 294);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (1998, 7, 1, 152, 'completed', '{"4956": 18961, "4957": 18966, "4958": 18967, "4959": 18970, "4960": 18973, "4961": 18976, "4962": 18979, "4963": 18982}', '2025-10-27 03:30:25.480531+00', '2025-10-27 03:32:57.480531+00', 526, 294);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (1999, 6, 2, 336, 'completed', '{"5028": 19177, "5029": 19182, "5030": 19183, "5031": 19186, "5032": 19189, "5033": 19193, "5034": 19195, "5035": 19198}', '2025-05-29 22:47:54+00', '2025-05-29 22:53:30+00', 535, 294);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2000, 2, 1, 87, 'in_progress', '{"4948": 18930, "4949": 18935, "4954": 18953}', '2026-01-31 09:18:55+00', '2026-01-31 09:19:15+00', 525, 294);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2001, 0, 1, 18, 'in_progress', '{"4904": 18756}', '2024-10-04 12:27:19.480531+00', '2024-10-04 12:27:29.480531+00', 520, 294);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2002, 1, 1, 44, 'in_progress', '{"4940": 18897, "4944": 18916}', '2026-01-01 13:23:49.480531+00', '2026-01-01 13:24:06.480531+00', 524, 294);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2003, 2, 1, 42, 'in_progress', '{"4999": 19091, "5000": 19093, "5003": 19102}', '2025-12-28 14:10:35.480531+00', '2025-12-28 14:10:59.480531+00', 531, 294);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2004, 4, 4, 296, 'completed', '{"4964": 18986, "4965": 18988, "4966": 18991, "4967": 18994, "4968": 18998, "4969": 19000, "4970": 19004, "4971": 19007}', '2024-12-12 17:07:34+00', '2024-12-12 17:12:30+00', 527, 295);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2005, 7, 1, 184, 'completed', '{"4895": 18718, "4896": 18721, "4897": 18726, "4898": 18730, "4899": 18734, "4900": 18738, "4901": 18741, "4902": 18745}', '2024-11-25 15:26:38+00', '2024-11-25 15:29:42+00', 519, 295);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2006, 1, 7, 240, 'completed', '{"5012": 19130, "5013": 19134, "5014": 19136, "5015": 19139, "5016": 19142, "5017": 19144, "5018": 19149, "5019": 19151}', '2025-09-06 23:27:16+00', '2025-09-06 23:31:16+00', 533, 295);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2007, 3, 5, 360, 'completed', '{"4996": 19083, "4997": 19084, "4998": 19088, "4999": 19092, "5000": 19094, "5001": 19096, "5002": 19099, "5003": 19103}', '2025-02-14 07:53:21.480531+00', '2025-02-14 07:59:21.480531+00', 531, 295);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2008, 0, 1, 27, 'in_progress', '{"5006": 19112}', '2025-01-31 15:22:57.480531+00', '2025-01-31 15:23:12.480531+00', 532, 295);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2009, 1, 1, 54, 'abandoned', '{"4932": 18866, "4935": 18877}', '2024-10-11 18:57:48+00', '2024-10-11 18:57:58+00', 523, 295);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2010, 3, 0, 135, 'abandoned', '{"5022": 19159, "5023": 19162, "5025": 19168}', '2026-03-21 12:25:19+00', '2026-03-21 12:26:20+00', 534, 295);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2011, 2, 6, 200, 'completed', '{"4920": 18817, "4921": 18822, "4922": 18825, "4923": 18832, "4924": 18833, "4925": 18839, "4926": 18844, "4927": 18847}', '2026-04-09 07:13:03+00', '2026-04-09 07:16:23+00', 522, 295);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2012, 2, 1, 96, 'in_progress', '{"4939": 18893, "4940": 18897, "4944": 18915}', '2025-11-07 01:09:04.480531+00', '2025-11-07 01:09:52.480531+00', 524, 296);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2013, 4, 1, 130, 'abandoned', '{"4877": 18646, "4878": 18649, "4879": 18654, "4882": 18666, "4884": 18674}', '2025-11-02 14:45:56+00', '2025-11-02 14:47:17+00', 517, 296);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2014, 8, 0, 232, 'completed', '{"4895": 18718, "4896": 18721, "4897": 18726, "4898": 18730, "4899": 18734, "4900": 18738, "4901": 18741, "4902": 18746}', '2025-05-22 01:41:44+00', '2025-05-22 01:45:36+00', 519, 296);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2015, 5, 3, 328, 'completed', '{"4980": 19035, "4981": 19036, "4982": 19040, "4983": 19042, "4984": 19045, "4985": 19048, "4986": 19051, "4987": 19055}', '2026-04-28 06:53:26+00', '2026-04-28 06:58:54+00', 529, 296);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2016, 4, 4, 304, 'completed', '{"4928": 18849, "4929": 18853, "4930": 18859, "4931": 18861, "4932": 18865, "4933": 18872, "4934": 18874, "4935": 18880}', '2025-03-27 20:48:26+00', '2025-03-27 20:53:30+00', 523, 296);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2017, 2, 2, 136, 'abandoned', '{"4948": 18930, "4949": 18933, "4953": 18949, "4954": 18954}', '2026-04-29 15:25:37+00', '2026-04-29 15:26:16+00', 525, 296);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2018, 4, 5, 369, 'completed', '{"4903": 18752, "4904": 18753, "4905": 18758, "4906": 18763, "4907": 18766, "4908": 18772, "4909": 18776, "4910": 18779, "4911": 18783}', '2024-07-19 08:07:36.480531+00', '2024-07-19 08:13:45.480531+00', 520, 296);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2019, 4, 4, 176, 'completed', '{"5012": 19131, "5013": 19132, "5014": 19136, "5015": 19138, "5016": 19141, "5017": 19145, "5018": 19147, "5019": 19151}', '2025-03-21 09:56:12+00', '2025-03-21 09:59:08+00', 533, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2020, 2, 0, 66, 'abandoned', '{"4879": 18654, "4884": 18674}', '2025-12-20 12:57:41+00', '2025-12-20 12:58:18+00', 517, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2021, 1, 0, 29, 'in_progress', '{"4914": 18794}', '2026-01-11 17:43:59+00', '2026-01-11 17:44:16+00', 521, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2022, 1, 3, 168, 'in_progress', '{"4972": 19010, "4973": 19013, "4975": 19019, "4976": 19021}', '2026-05-01 15:11:53+00', '2026-05-01 15:13:00+00', 528, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2023, 4, 0, 60, 'in_progress', '{"5021": 19156, "5022": 19159, "5023": 19162, "5026": 19171}', '2026-04-15 22:09:17+00', '2026-04-15 22:10:00+00', 534, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2024, 4, 4, 280, 'completed', '{"4956": 18963, "4957": 18965, "4958": 18968, "4959": 18970, "4960": 18973, "4961": 18976, "4962": 18980, "4963": 18982}', '2025-12-16 02:54:44.480531+00', '2025-12-16 02:59:24.480531+00', 526, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2025, 7, 1, 352, 'completed', '{"5028": 19177, "5029": 19181, "5030": 19183, "5031": 19186, "5032": 19189, "5033": 19192, "5034": 19195, "5035": 19198}', '2025-06-14 14:50:03+00', '2025-06-14 14:55:55+00', 535, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2026, 9, 1, 380, 'completed', '{"4946": 18923, "4947": 18926, "4948": 18930, "4949": 18934, "4950": 18938, "4951": 18942, "4952": 18948, "4953": 18949, "4954": 18953, "4955": 18958}', '2026-06-10 07:19:26+00', '2026-06-10 07:25:46+00', 525, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2027, 6, 2, 112, 'completed', '{"4988": 19059, "4989": 19062, "4990": 19063, "4991": 19066, "4992": 19069, "4993": 19072, "4994": 19075, "4995": 19078}', '2026-05-02 13:17:11+00', '2026-05-02 13:19:03+00', 530, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2028, 7, 2, 99, 'completed', '{"4858": 18569, "4859": 18573, "4860": 18578, "4861": 18581, "4862": 18586, "4863": 18592, "4864": 18596, "4865": 18598, "4866": 18604}', '2024-09-05 17:31:17.480531+00', '2024-09-05 17:32:56.480531+00', 515, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2029, 6, 2, 360, 'completed', '{"4996": 19081, "4997": 19084, "4998": 19087, "4999": 19092, "5000": 19093, "5001": 19098, "5002": 19099, "5003": 19102}', '2024-07-25 07:08:56.480531+00', '2024-07-25 07:14:56.480531+00', 531, 297);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2030, 2, 6, 328, 'completed', '{"4964": 18986, "4965": 18989, "4966": 18991, "4967": 18996, "4968": 18999, "4969": 19000, "4970": 19005, "4971": 19008}', '2026-01-30 19:06:56+00', '2026-01-30 19:12:24+00', 527, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2031, 1, 7, 248, 'completed', '{"5012": 19131, "5013": 19134, "5014": 19137, "5015": 19140, "5016": 19142, "5017": 19144, "5018": 19149, "5019": 19152}', '2026-05-08 06:30:43+00', '2026-05-08 06:34:51+00', 533, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2032, 4, 0, 136, 'abandoned', '{"4887": 18685, "4891": 18702, "4892": 18706, "4893": 18710}', '2026-01-09 01:31:38+00', '2026-01-09 01:33:09+00', 518, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2033, 0, 2, 32, 'abandoned', '{"4858": 18571, "4865": 18599}', '2025-08-09 07:30:13.480531+00', '2025-08-09 07:30:36.480531+00', 515, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2034, 7, 3, 110, 'completed', '{"4936": 18882, "4937": 18885, "4938": 18892, "4939": 18893, "4940": 18900, "4941": 18901, "4942": 18905, "4943": 18909, "4944": 18913, "4945": 18917}', '2024-08-01 12:23:55.480531+00', '2024-08-01 12:25:45.480531+00', 524, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2035, 3, 6, 342, 'completed', '{"4877": 18646, "4878": 18649, "4879": 18656, "4880": 18659, "4881": 18661, "4882": 18666, "4883": 18670, "4884": 18676, "4885": 18679}', '2026-02-27 13:57:30+00', '2026-02-27 14:03:12+00', 517, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2036, 2, 1, 84, 'in_progress', '{"4906": 18761, "4907": 18765, "4909": 18773}', '2025-12-21 22:34:18.480531+00', '2025-12-21 22:34:49.480531+00', 520, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2037, 4, 0, 104, 'in_progress', '{"4920": 18817, "4924": 18833, "4926": 18841, "4927": 18846}', '2026-03-15 01:15:00+00', '2026-03-15 01:16:00+00', 522, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2038, 1, 0, 18, 'in_progress', '{"4960": 18973}', '2024-09-04 19:16:22.480531+00', '2024-09-04 19:16:35.480531+00', 526, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2039, 0, 8, 120, 'completed', '{"5028": 19179, "5029": 19182, "5030": 19184, "5031": 19187, "5032": 19191, "5033": 19194, "5034": 19197, "5035": 19200}', '2026-01-08 18:33:35+00', '2026-01-08 18:35:35+00', 535, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2040, 6, 2, 352, 'completed', '{"4972": 19009, "4973": 19012, "4974": 19015, "4975": 19019, "4976": 19021, "4977": 19026, "4978": 19027, "4979": 19030}', '2025-03-30 01:04:41+00', '2025-03-30 01:10:33+00', 528, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2041, 6, 2, 176, 'completed', '{"4928": 18850, "4929": 18853, "4930": 18857, "4931": 18863, "4932": 18865, "4933": 18872, "4934": 18874, "4935": 18877}', '2024-12-11 10:20:55+00', '2024-12-11 10:23:51+00', 523, 298);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2042, 8, 0, 344, 'completed', '{"4964": 18985, "4965": 18988, "4966": 18991, "4967": 18994, "4968": 18997, "4969": 19000, "4970": 19003, "4971": 19006}', '2024-10-19 11:14:16+00', '2024-10-19 11:20:00+00', 527, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2043, 1, 4, 175, 'abandoned', '{"4947": 18927, "4949": 18933, "4950": 18938, "4951": 18944, "4953": 18952}', '2026-03-08 15:57:56+00', '2026-03-08 15:59:43+00', 525, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2044, 7, 1, 240, 'completed', '{"4956": 18961, "4957": 18965, "4958": 18967, "4959": 18970, "4960": 18973, "4961": 18976, "4962": 18979, "4963": 18982}', '2025-05-24 06:31:21.480531+00', '2025-05-24 06:35:21.480531+00', 526, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2045, 3, 5, 128, 'completed', '{"4895": 18718, "4896": 18721, "4897": 18728, "4898": 18731, "4899": 18735, "4900": 18739, "4901": 18741, "4902": 18748}', '2026-01-03 02:25:06+00', '2026-01-03 02:27:14+00', 519, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2046, 6, 2, 112, 'completed', '{"5012": 19129, "5013": 19132, "5014": 19135, "5015": 19138, "5016": 19143, "5017": 19145, "5018": 19147, "5019": 19150}', '2025-06-23 18:45:39+00', '2025-06-23 18:47:31+00', 533, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2047, 1, 0, 39, 'abandoned', '{"4929": 18853}', '2025-05-30 07:53:18+00', '2025-05-30 07:53:29+00', 523, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2048, 7, 1, 96, 'completed', '{"4996": 19082, "4997": 19084, "4998": 19087, "4999": 19090, "5000": 19093, "5001": 19096, "5002": 19099, "5003": 19102}', '2024-12-15 01:49:35.480531+00', '2024-12-15 01:51:11.480531+00', 531, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2049, 2, 7, 333, 'completed', '{"4877": 18647, "4878": 18650, "4879": 18656, "4880": 18658, "4881": 18664, "4882": 18666, "4883": 18669, "4884": 18676, "4885": 18677}', '2026-05-27 01:31:32+00', '2026-05-27 01:37:05+00', 517, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2050, 6, 2, 256, 'completed', '{"4988": 19057, "4989": 19060, "4990": 19063, "4991": 19066, "4992": 19069, "4993": 19074, "4994": 19076, "4995": 19078}', '2026-02-26 06:05:02+00', '2026-02-26 06:09:18+00', 530, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2051, 2, 1, 117, 'abandoned', '{"4937": 18888, "4938": 18889, "4939": 18893}', '2026-02-02 18:57:16.480531+00', '2026-02-02 18:58:18.480531+00', 524, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2052, 6, 2, 304, 'completed', '{"5028": 19179, "5029": 19180, "5030": 19183, "5031": 19186, "5032": 19189, "5033": 19192, "5034": 19197, "5035": 19198}', '2026-05-26 07:36:35+00', '2026-05-26 07:41:39+00', 535, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2053, 1, 2, 36, 'abandoned', '{"4886": 18682, "4888": 18690, "4893": 18711}', '2025-02-19 23:44:54+00', '2025-02-19 23:45:16+00', 518, 299);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2054, 2, 6, 336, 'completed', '{"5004": 19107, "5005": 19110, "5006": 19113, "5007": 19114, "5008": 19119, "5009": 19121, "5010": 19123, "5011": 19127}', '2025-04-03 20:01:46.480531+00', '2025-04-03 20:07:22.480531+00', 532, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2055, 2, 6, 304, 'completed', '{"4996": 19082, "4997": 19085, "4998": 19088, "4999": 19090, "5000": 19093, "5001": 19098, "5002": 19100, "5003": 19103}', '2024-12-25 13:11:45.480531+00', '2024-12-25 13:16:49.480531+00', 531, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2056, 3, 5, 224, 'completed', '{"4912": 18786, "4913": 18789, "4914": 18794, "4915": 18800, "4916": 18804, "4917": 18808, "4918": 18809, "4919": 18816}', '2025-07-04 16:41:29+00', '2025-07-04 16:45:13+00', 521, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2057, 1, 3, 100, 'abandoned', '{"4869": 18615, "4873": 18629, "4874": 18633, "4875": 18639}', '2026-01-30 01:06:45+00', '2026-01-30 01:08:04+00', 516, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2058, 7, 1, 104, 'completed', '{"5028": 19177, "5029": 19180, "5030": 19183, "5031": 19186, "5032": 19189, "5033": 19192, "5034": 19196, "5035": 19198}', '2025-09-09 11:59:29+00', '2025-09-09 12:01:13+00', 535, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2059, 6, 2, 88, 'completed', '{"4988": 19057, "4989": 19062, "4990": 19063, "4991": 19068, "4992": 19069, "4993": 19072, "4994": 19075, "4995": 19078}', '2026-02-27 10:01:07+00', '2026-02-27 10:02:35+00', 530, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2060, 1, 3, 56, 'abandoned', '{"4947": 18926, "4949": 18936, "4951": 18943, "4954": 18954}', '2026-05-03 22:23:54+00', '2026-05-03 22:24:31+00', 525, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2061, 8, 0, 328, 'completed', '{"4972": 19009, "4973": 19012, "4974": 19015, "4975": 19018, "4976": 19021, "4977": 19024, "4978": 19027, "4979": 19030}', '2026-06-05 05:12:31+00', '2026-06-05 05:17:59+00', 528, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2062, 7, 2, 99, 'completed', '{"4877": 18646, "4878": 18649, "4879": 18654, "4880": 18659, "4881": 18662, "4882": 18667, "4883": 18670, "4884": 18674, "4885": 18677}', '2025-12-10 19:51:15+00', '2025-12-10 19:52:54+00', 517, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2063, 2, 2, 152, 'in_progress', '{"4920": 18817, "4921": 18822, "4926": 18843, "4927": 18846}', '2026-03-03 10:07:29+00', '2026-03-03 10:08:51+00', 522, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2064, 4, 4, 120, 'completed', '{"5012": 19129, "5013": 19134, "5014": 19135, "5015": 19138, "5016": 19143, "5017": 19145, "5018": 19147, "5019": 19152}', '2025-11-08 19:34:25+00', '2025-11-08 19:36:25+00', 533, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2065, 0, 1, 33, 'abandoned', '{"4984": 19046}', '2026-06-09 15:48:12+00', '2026-06-09 15:48:23+00', 529, 300);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2066, 0, 2, 28, 'in_progress', '{"5020": 19155, "5021": 19158}', '2026-03-17 02:19:12+00', '2026-03-17 02:19:33+00', 534, 301);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2067, 0, 4, 68, 'abandoned', '{"4930": 18858, "4932": 18866, "4933": 18870, "4935": 18880}', '2025-10-14 23:15:01+00', '2025-10-14 23:15:20+00', 523, 301);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2068, 6, 2, 184, 'completed', '{"4980": 19034, "4981": 19036, "4982": 19039, "4983": 19042, "4984": 19045, "4985": 19048, "4986": 19052, "4987": 19054}', '2026-05-04 20:43:34+00', '2026-05-04 20:46:38+00', 529, 301);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2069, 1, 0, 40, 'abandoned', '{"4963": 18982}', '2025-01-02 23:55:12.480531+00', '2025-01-02 23:55:39.480531+00', 526, 301);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2070, 3, 1, 140, 'abandoned', '{"4867": 18606, "4868": 18610, "4874": 18634, "4875": 18639}', '2025-07-15 16:06:43+00', '2025-07-15 16:08:14+00', 516, 301);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2071, 3, 5, 280, 'completed', '{"5004": 19105, "5005": 19108, "5006": 19113, "5007": 19116, "5008": 19118, "5009": 19122, "5010": 19125, "5011": 19126}', '2025-07-24 09:13:57.480531+00', '2025-07-24 09:18:37.480531+00', 532, 301);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2072, 6, 3, 153, 'completed', '{"4858": 18569, "4859": 18573, "4860": 18578, "4861": 18581, "4862": 18587, "4863": 18591, "4864": 18596, "4865": 18600, "4866": 18601}', '2024-10-04 17:31:27.480531+00', '2024-10-04 17:34:00.480531+00', 515, 301);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2073, 3, 1, 156, 'in_progress', '{"4879": 18656, "4881": 18662, "4882": 18665, "4885": 18677}', '2025-12-13 05:16:51+00', '2025-12-13 05:18:18+00', 517, 301);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2074, 7, 1, 288, 'completed', '{"5020": 19153, "5021": 19156, "5022": 19161, "5023": 19162, "5024": 19165, "5025": 19168, "5026": 19171, "5027": 19174}', '2026-05-29 04:54:12+00', '2026-05-29 04:59:00+00', 534, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2075, 1, 3, 176, 'abandoned', '{"5012": 19129, "5013": 19134, "5016": 19143, "5017": 19146}', '2025-12-05 18:24:50+00', '2025-12-05 18:26:36+00', 533, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2076, 2, 1, 90, 'in_progress', '{"4859": 18573, "4861": 18584, "4865": 18598}', '2025-07-04 11:14:56.480531+00', '2025-07-04 11:15:32.480531+00', 515, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2077, 2, 1, 45, 'in_progress', '{"4912": 18786, "4916": 18801, "4919": 18813}', '2025-10-14 15:15:37+00', '2025-10-14 15:16:10+00', 521, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2078, 2, 2, 64, 'abandoned', '{"4880": 18659, "4881": 18661, "4883": 18670, "4885": 18677}', '2026-03-25 21:18:04+00', '2026-03-25 21:18:29+00', 517, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2079, 4, 4, 280, 'completed', '{"4988": 19057, "4989": 19060, "4990": 19065, "4991": 19066, "4992": 19070, "4993": 19072, "4994": 19076, "4995": 19079}', '2026-05-22 02:00:11+00', '2026-05-22 02:04:51+00', 530, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2080, 8, 0, 168, 'completed', '{"4980": 19033, "4981": 19036, "4982": 19039, "4983": 19042, "4984": 19045, "4985": 19048, "4986": 19051, "4987": 19054}', '2026-04-30 13:18:01+00', '2026-04-30 13:20:49+00', 529, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2081, 2, 1, 75, 'in_progress', '{"5029": 19182, "5031": 19186, "5033": 19192}', '2026-02-18 06:54:38+00', '2026-02-18 06:55:26+00', 535, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2082, 3, 0, 51, 'in_progress', '{"4886": 18682, "4890": 18698, "4891": 18702}', '2025-12-20 15:54:46+00', '2025-12-20 15:55:24+00', 518, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2083, 6, 2, 328, 'completed', '{"5004": 19105, "5005": 19109, "5006": 19111, "5007": 19115, "5008": 19117, "5009": 19120, "5010": 19123, "5011": 19126}', '2024-09-05 10:20:24.480531+00', '2024-09-05 10:25:52.480531+00', 532, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2084, 2, 2, 92, 'in_progress', '{"4867": 18608, "4869": 18615, "4871": 18622, "4874": 18634}', '2025-05-31 19:49:24+00', '2025-05-31 19:49:44+00', 516, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2085, 4, 4, 88, 'completed', '{"4928": 18851, "4929": 18853, "4930": 18858, "4931": 18863, "4932": 18865, "4933": 18869, "4934": 18874, "4935": 18880}', '2025-04-27 07:00:57+00', '2025-04-27 07:02:25+00', 523, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2086, 6, 2, 352, 'completed', '{"4996": 19081, "4997": 19084, "4998": 19087, "4999": 19091, "5000": 19093, "5001": 19096, "5002": 19100, "5003": 19102}', '2024-12-12 13:15:23.480531+00', '2024-12-12 13:21:15.480531+00', 531, 302);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2087, 2, 6, 200, 'completed', '{"5020": 19153, "5021": 19158, "5022": 19160, "5023": 19164, "5024": 19167, "5025": 19169, "5026": 19173, "5027": 19174}', '2026-04-05 12:26:12+00', '2026-04-05 12:29:32+00', 534, 303);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2088, 3, 5, 232, 'completed', '{"5004": 19105, "5005": 19109, "5006": 19111, "5007": 19114, "5008": 19118, "5009": 19121, "5010": 19125, "5011": 19128}', '2026-06-02 19:56:39.480531+00', '2026-06-02 20:00:31.480531+00', 532, 303);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2089, 7, 1, 192, 'completed', '{"4988": 19057, "4989": 19060, "4990": 19063, "4991": 19066, "4992": 19069, "4993": 19072, "4994": 19077, "4995": 19078}', '2026-05-13 00:19:37+00', '2026-05-13 00:22:49+00', 530, 303);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2090, 4, 4, 168, 'completed', '{"4928": 18850, "4929": 18855, "4930": 18857, "4931": 18864, "4932": 18865, "4933": 18869, "4934": 18875, "4935": 18880}', '2025-11-02 15:17:24+00', '2025-11-02 15:20:12+00', 523, 303);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2091, 1, 0, 10, 'in_progress', '{"5012": 19129}', '2026-01-19 21:34:26+00', '2026-01-19 21:34:28+00', 533, 303);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2092, 4, 4, 312, 'completed', '{"4928": 18849, "4929": 18854, "4930": 18857, "4931": 18863, "4932": 18865, "4933": 18869, "4934": 18875, "4935": 18877}', '2025-11-20 09:31:50+00', '2025-11-20 09:37:02+00', 523, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2093, 4, 4, 216, 'completed', '{"4964": 18987, "4965": 18988, "4966": 18992, "4967": 18994, "4968": 18998, "4969": 19000, "4970": 19003, "4971": 19007}', '2025-09-17 23:29:14+00', '2025-09-17 23:32:50+00', 527, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2094, 8, 0, 248, 'completed', '{"5020": 19153, "5021": 19156, "5022": 19159, "5023": 19162, "5024": 19165, "5025": 19168, "5026": 19171, "5027": 19174}', '2026-06-16 09:59:33+00', '2026-06-16 10:03:41+00', 534, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2095, 5, 3, 80, 'completed', '{"4956": 18963, "4957": 18964, "4958": 18968, "4959": 18970, "4960": 18973, "4961": 18976, "4962": 18981, "4963": 18982}', '2025-02-21 05:35:12.480531+00', '2025-02-21 05:36:32.480531+00', 526, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2096, 3, 7, 140, 'completed', '{"4946": 18923, "4947": 18927, "4948": 18929, "4949": 18933, "4950": 18937, "4951": 18942, "4952": 18946, "4953": 18950, "4954": 18956, "4955": 18957}', '2026-01-17 08:37:46+00', '2026-01-17 08:40:06+00', 525, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2097, 4, 4, 320, 'completed', '{"4972": 19011, "4973": 19012, "4974": 19015, "4975": 19020, "4976": 19022, "4977": 19024, "4978": 19027, "4979": 19032}', '2025-08-15 16:55:04+00', '2025-08-15 17:00:24+00', 528, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2098, 4, 4, 288, 'completed', '{"4912": 18786, "4913": 18791, "4914": 18793, "4915": 18798, "4916": 18802, "4917": 18805, "4918": 18809, "4919": 18813}', '2026-02-18 11:31:29+00', '2026-02-18 11:36:17+00', 521, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2099, 8, 0, 248, 'completed', '{"5028": 19177, "5029": 19180, "5030": 19183, "5031": 19186, "5032": 19189, "5033": 19192, "5034": 19195, "5035": 19198}', '2026-02-05 15:25:47+00', '2026-02-05 15:29:55+00', 535, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2100, 7, 1, 320, 'completed', '{"4988": 19057, "4989": 19061, "4990": 19063, "4991": 19066, "4992": 19069, "4993": 19072, "4994": 19075, "4995": 19078}', '2026-01-08 00:47:48+00', '2026-01-08 00:53:08+00', 530, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2101, 6, 2, 304, 'completed', '{"5012": 19129, "5013": 19132, "5014": 19136, "5015": 19138, "5016": 19141, "5017": 19145, "5018": 19147, "5019": 19150}', '2026-06-08 13:29:34+00', '2026-06-08 13:34:38+00', 533, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2102, 5, 5, 300, 'completed', '{"4867": 18606, "4868": 18610, "4869": 18614, "4870": 18619, "4871": 18624, "4872": 18628, "4873": 18629, "4874": 18636, "4875": 18640, "4876": 18642}', '2025-07-05 15:33:17+00', '2025-07-05 15:38:17+00', 516, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2103, 4, 5, 369, 'completed', '{"4877": 18648, "4878": 18649, "4879": 18655, "4880": 18659, "4881": 18662, "4882": 18665, "4883": 18671, "4884": 18674, "4885": 18679}', '2026-03-26 19:00:35+00', '2026-03-26 19:06:44+00', 517, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2104, 1, 3, 180, 'abandoned', '{"4996": 19082, "4997": 19084, "5000": 19095, "5003": 19104}', '2025-07-28 13:10:43.480531+00', '2025-07-28 13:11:31.480531+00', 531, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2105, 3, 6, 288, 'completed', '{"4886": 18681, "4887": 18688, "4888": 18690, "4889": 18694, "4890": 18698, "4891": 18702, "4892": 18705, "4893": 18709, "4894": 18715}', '2025-09-28 23:54:14+00', '2025-09-28 23:59:02+00', 518, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2106, 1, 8, 342, 'completed', '{"4903": 18751, "4904": 18755, "4905": 18759, "4906": 18762, "4907": 18768, "4908": 18770, "4909": 18773, "4910": 18778, "4911": 18782}', '2024-08-24 10:47:25.480531+00', '2024-08-24 10:53:07.480531+00', 520, 304);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2107, 5, 3, 160, 'completed', '{"4964": 18987, "4965": 18988, "4966": 18991, "4967": 18994, "4968": 18997, "4969": 19002, "4970": 19003, "4971": 19007}', '2026-06-02 09:05:39+00', '2026-06-02 09:08:19+00', 527, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2108, 1, 2, 72, 'in_progress', '{"4878": 18652, "4879": 18656, "4882": 18665}', '2026-04-01 01:46:32+00', '2026-04-01 01:47:14+00', 517, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2109, 1, 0, 43, 'abandoned', '{"5007": 19114}', '2025-12-06 22:51:42.480531+00', '2025-12-06 22:52:02.480531+00', 532, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2110, 4, 5, 342, 'completed', '{"4886": 18684, "4887": 18685, "4888": 18689, "4889": 18696, "4890": 18700, "4891": 18701, "4892": 18706, "4893": 18710, "4894": 18713}', '2026-06-10 12:20:03+00', '2026-06-10 12:25:45+00', 518, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2111, 3, 7, 430, 'completed', '{"4867": 18606, "4868": 18609, "4869": 18616, "4870": 18618, "4871": 18624, "4872": 18625, "4873": 18630, "4874": 18633, "4875": 18639, "4876": 18643}', '2025-04-14 11:23:59+00', '2025-04-14 11:31:09+00', 516, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2112, 2, 1, 30, 'in_progress', '{"4974": 19015, "4975": 19019, "4976": 19021}', '2025-07-06 07:36:17+00', '2025-07-06 07:36:26+00', 528, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2113, 4, 0, 76, 'in_progress', '{"4932": 18865, "4933": 18869, "4934": 18874, "4935": 18877}', '2025-10-29 04:09:51+00', '2025-10-29 04:10:21+00', 523, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2114, 8, 0, 136, 'completed', '{"4912": 18785, "4913": 18789, "4914": 18794, "4915": 18798, "4916": 18801, "4917": 18805, "4918": 18809, "4919": 18813}', '2026-03-28 17:10:12+00', '2026-03-28 17:12:28+00', 521, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2115, 1, 2, 99, 'in_progress', '{"4990": 19065, "4992": 19069, "4994": 19076}', '2026-01-19 14:57:29+00', '2026-01-19 14:58:03+00', 530, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2116, 3, 5, 168, 'completed', '{"4956": 18963, "4957": 18965, "4958": 18968, "4959": 18970, "4960": 18973, "4961": 18978, "4962": 18980, "4963": 18982}', '2024-12-17 03:32:09.480531+00', '2024-12-17 03:34:57.480531+00', 526, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2117, 0, 1, 29, 'in_progress', '{"4901": 18743}', '2025-06-22 10:34:04+00', '2025-06-22 10:34:11+00', 519, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2118, 2, 6, 128, 'completed', '{"4980": 19035, "4981": 19037, "4982": 19039, "4983": 19043, "4984": 19045, "4985": 19049, "4986": 19053, "4987": 19055}', '2026-02-11 18:24:22+00', '2026-02-11 18:26:30+00', 529, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2119, 8, 1, 270, 'completed', '{"4903": 18750, "4904": 18753, "4905": 18758, "4906": 18761, "4907": 18766, "4908": 18769, "4909": 18773, "4910": 18779, "4911": 18783}', '2025-06-13 11:04:59.480531+00', '2025-06-13 11:09:29.480531+00', 520, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2120, 7, 1, 256, 'completed', '{"5012": 19129, "5013": 19132, "5014": 19135, "5015": 19139, "5016": 19141, "5017": 19144, "5018": 19147, "5019": 19150}', '2026-01-07 08:33:28+00', '2026-01-07 08:37:44+00', 533, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2121, 7, 3, 170, 'completed', '{"4946": 18923, "4947": 18926, "4948": 18930, "4949": 18934, "4950": 18938, "4951": 18941, "4952": 18946, "4953": 18951, "4954": 18954, "4955": 18958}', '2025-12-24 04:21:57+00', '2025-12-24 04:24:47+00', 525, 305);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2122, 4, 4, 256, 'completed', '{"4895": 18719, "4896": 18724, "4897": 18727, "4898": 18730, "4899": 18734, "4900": 18739, "4901": 18741, "4902": 18746}', '2025-12-24 13:44:14+00', '2025-12-24 13:48:30+00', 519, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2123, 7, 1, 256, 'completed', '{"4912": 18786, "4913": 18789, "4914": 18794, "4915": 18798, "4916": 18801, "4917": 18805, "4918": 18809, "4919": 18813}', '2026-05-31 07:40:14+00', '2026-05-31 07:44:30+00', 521, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2124, 1, 1, 64, 'in_progress', '{"4921": 18821, "4922": 18828}', '2026-06-06 17:15:35+00', '2026-06-06 17:16:09+00', 522, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2125, 4, 5, 144, 'completed', '{"4903": 18752, "4904": 18753, "4905": 18759, "4906": 18761, "4907": 18767, "4908": 18770, "4909": 18773, "4910": 18777, "4911": 18781}', '2025-03-15 05:01:05.480531+00', '2025-03-15 05:03:29.480531+00', 520, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2126, 5, 4, 279, 'completed', '{"4877": 18648, "4878": 18649, "4879": 18655, "4880": 18660, "4881": 18661, "4882": 18665, "4883": 18670, "4884": 18674, "4885": 18677}', '2025-11-15 14:15:49+00', '2025-11-15 14:20:28+00', 517, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2127, 4, 4, 192, 'completed', '{"4980": 19033, "4981": 19036, "4982": 19041, "4983": 19042, "4984": 19045, "4985": 19050, "4986": 19053, "4987": 19055}', '2026-01-26 05:55:28+00', '2026-01-26 05:58:40+00', 529, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2128, 4, 4, 288, 'completed', '{"4956": 18961, "4957": 18964, "4958": 18968, "4959": 18970, "4960": 18974, "4961": 18978, "4962": 18981, "4963": 18982}', '2025-12-20 07:45:12.480531+00', '2025-12-20 07:50:00.480531+00', 526, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2129, 6, 4, 330, 'completed', '{"4946": 18922, "4947": 18927, "4948": 18930, "4949": 18934, "4950": 18938, "4951": 18944, "4952": 18946, "4953": 18951, "4954": 18953, "4955": 18958}', '2026-01-21 02:55:34+00', '2026-01-21 03:01:04+00', 525, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2130, 5, 3, 280, 'completed', '{"5012": 19129, "5013": 19134, "5014": 19135, "5015": 19138, "5016": 19141, "5017": 19146, "5018": 19148, "5019": 19150}', '2025-04-01 13:24:42+00', '2025-04-01 13:29:22+00', 533, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2131, 4, 4, 136, 'completed', '{"5028": 19177, "5029": 19180, "5030": 19183, "5031": 19188, "5032": 19189, "5033": 19194, "5034": 19197, "5035": 19199}', '2026-01-24 04:55:23+00', '2026-01-24 04:57:39+00', 535, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2132, 4, 4, 232, 'completed', '{"4964": 18985, "4965": 18990, "4966": 18992, "4967": 18996, "4968": 18997, "4969": 19000, "4970": 19003, "4971": 19007}', '2025-02-25 22:42:06+00', '2025-02-25 22:45:58+00', 527, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2133, 0, 1, 30, 'in_progress', '{"4861": 18583}', '2025-01-22 01:25:02.480531+00', '2025-01-22 01:25:21.480531+00', 515, 306);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2134, 8, 0, 360, 'completed', '{"4996": 19081, "4997": 19084, "4998": 19087, "4999": 19090, "5000": 19093, "5001": 19096, "5002": 19099, "5003": 19102}', '2025-03-25 11:03:43.480531+00', '2025-03-25 11:09:43.480531+00', 531, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2135, 1, 7, 216, 'completed', '{"4964": 18986, "4965": 18989, "4966": 18992, "4967": 18994, "4968": 18998, "4969": 19001, "4970": 19005, "4971": 19007}', '2025-06-17 08:59:33+00', '2025-06-17 09:03:09+00', 527, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2136, 2, 1, 135, 'in_progress', '{"4949": 18934, "4950": 18938, "4953": 18952}', '2026-04-20 14:13:10+00', '2026-04-20 14:14:25+00', 525, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2137, 2, 6, 176, 'completed', '{"4972": 19011, "4973": 19014, "4974": 19016, "4975": 19018, "4976": 19023, "4977": 19024, "4978": 19029, "4979": 19032}', '2025-09-07 05:12:51+00', '2025-09-07 05:15:47+00', 528, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2138, 1, 1, 42, 'abandoned', '{"4925": 18840, "4927": 18846}', '2026-04-14 12:56:44+00', '2026-04-14 12:56:54+00', 522, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2139, 8, 1, 279, 'completed', '{"4903": 18750, "4904": 18753, "4905": 18758, "4906": 18761, "4907": 18767, "4908": 18769, "4909": 18773, "4910": 18777, "4911": 18783}', '2025-05-10 14:57:13.480531+00', '2025-05-10 15:01:52.480531+00', 520, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2140, 4, 0, 80, 'in_progress', '{"4869": 18614, "4872": 18625, "4873": 18629, "4876": 18642}', '2026-04-20 08:49:58+00', '2026-04-20 08:50:51+00', 516, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2141, 2, 0, 88, 'abandoned', '{"4933": 18869, "4934": 18874}', '2025-02-09 10:28:39+00', '2025-02-09 10:29:35+00', 523, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2142, 3, 0, 102, 'in_progress', '{"4877": 18646, "4880": 18658, "4885": 18677}', '2026-04-29 20:29:21+00', '2026-04-29 20:30:17+00', 517, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2143, 9, 0, 117, 'completed', '{"4886": 18682, "4887": 18685, "4888": 18689, "4889": 18694, "4890": 18698, "4891": 18702, "4892": 18706, "4893": 18710, "4894": 18714}', '2026-01-07 17:29:04+00', '2026-01-07 17:31:01+00', 518, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2144, 7, 1, 328, 'completed', '{"4912": 18785, "4913": 18789, "4914": 18794, "4915": 18798, "4916": 18801, "4917": 18805, "4918": 18811, "4919": 18813}', '2025-08-18 06:26:22+00', '2025-08-18 06:31:50+00', 521, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2145, 2, 1, 30, 'abandoned', '{"4958": 18969, "4959": 18970, "4961": 18976}', '2025-11-30 11:12:50.480531+00', '2025-11-30 11:12:57.480531+00', 526, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2146, 7, 1, 160, 'completed', '{"5028": 19177, "5029": 19180, "5030": 19183, "5031": 19186, "5032": 19191, "5033": 19192, "5034": 19195, "5035": 19198}', '2025-11-18 13:50:19+00', '2025-11-18 13:52:59+00', 535, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2147, 4, 5, 288, 'completed', '{"4858": 18570, "4859": 18573, "4860": 18578, "4861": 18584, "4862": 18587, "4863": 18592, "4864": 18596, "4865": 18598, "4866": 18602}', '2025-10-14 15:36:43.480531+00', '2025-10-14 15:41:31.480531+00', 515, 307);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2148, 6, 2, 240, 'completed', '{"5020": 19153, "5021": 19157, "5022": 19159, "5023": 19163, "5024": 19165, "5025": 19168, "5026": 19171, "5027": 19174}', '2026-04-08 12:53:32+00', '2026-04-08 12:57:32+00', 534, 308);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2149, 4, 4, 312, 'completed', '{"4980": 19033, "4981": 19037, "4982": 19040, "4983": 19042, "4984": 19047, "4985": 19048, "4986": 19053, "4987": 19054}', '2026-04-05 10:50:51+00', '2026-04-05 10:56:03+00', 529, 308);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2150, 4, 5, 207, 'completed', '{"4858": 18570, "4859": 18573, "4860": 18577, "4861": 18581, "4862": 18586, "4863": 18591, "4864": 18594, "4865": 18599, "4866": 18601}', '2025-06-16 19:01:12.480531+00', '2025-06-16 19:04:39.480531+00', 515, 308);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2151, 1, 1, 78, 'in_progress', '{"4937": 18887, "4941": 18901}', '2025-11-20 05:35:14.480531+00', '2025-11-20 05:35:57.480531+00', 524, 308);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2152, 6, 3, 270, 'completed', '{"4903": 18750, "4904": 18753, "4905": 18757, "4906": 18763, "4907": 18766, "4908": 18769, "4909": 18776, "4910": 18777, "4911": 18783}', '2025-12-31 17:21:53.480531+00', '2025-12-31 17:26:23.480531+00', 520, 308);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2153, 7, 1, 184, 'completed', '{"4996": 19081, "4997": 19084, "4998": 19087, "4999": 19090, "5000": 19095, "5001": 19096, "5002": 19099, "5003": 19102}', '2026-02-02 03:04:27.480531+00', '2026-02-02 03:07:31.480531+00', 531, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2154, 5, 5, 220, 'completed', '{"4946": 18923, "4947": 18927, "4948": 18932, "4949": 18936, "4950": 18938, "4951": 18944, "4952": 18946, "4953": 18949, "4954": 18953, "4955": 18957}', '2026-02-11 00:21:15+00', '2026-02-11 00:24:55+00', 525, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2155, 5, 4, 387, 'completed', '{"4858": 18572, "4859": 18573, "4860": 18579, "4861": 18581, "4862": 18586, "4863": 18590, "4864": 18595, "4865": 18598, "4866": 18601}', '2024-12-14 15:27:14.480531+00', '2024-12-14 15:33:41.480531+00', 515, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2156, 1, 0, 32, 'in_progress', '{"4922": 18826}', '2026-03-31 10:40:13+00', '2026-03-31 10:40:36+00', 522, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2157, 2, 1, 114, 'abandoned', '{"4989": 19060, "4990": 19064, "4993": 19072}', '2026-02-04 17:56:34+00', '2026-02-04 17:57:58+00', 530, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2158, 3, 3, 96, 'abandoned', '{"4867": 18607, "4870": 18617, "4872": 18628, "4873": 18629, "4875": 18638, "4876": 18642}', '2025-08-13 02:55:11+00', '2025-08-13 02:56:26+00', 516, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2159, 0, 1, 37, 'abandoned', '{"4973": 19013}', '2025-03-05 09:27:11+00', '2025-03-05 09:27:22+00', 528, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2160, 2, 2, 104, 'in_progress', '{"5013": 19133, "5017": 19144, "5018": 19147, "5019": 19151}', '2026-01-16 04:51:05+00', '2026-01-16 04:51:50+00', 533, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2161, 1, 3, 112, 'abandoned', '{"4964": 18986, "4967": 18995, "4969": 19001, "4970": 19003}', '2026-03-26 09:23:22+00', '2026-03-26 09:24:30+00', 527, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2162, 3, 0, 57, 'abandoned', '{"4983": 19042, "4986": 19051, "4987": 19054}', '2026-03-19 19:56:38+00', '2026-03-19 19:57:12+00', 529, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2163, 1, 2, 69, 'in_progress', '{"4903": 18751, "4905": 18757, "4911": 18783}', '2025-05-13 07:30:08.480531+00', '2025-05-13 07:30:59.480531+00', 520, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2164, 1, 1, 90, 'in_progress', '{"4879": 18653, "4885": 18677}', '2026-04-13 12:21:23+00', '2026-04-13 12:22:15+00', 517, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2165, 8, 1, 333, 'completed', '{"4886": 18682, "4887": 18685, "4888": 18689, "4889": 18694, "4890": 18698, "4891": 18703, "4892": 18706, "4893": 18710, "4894": 18714}', '2025-03-14 11:09:24+00', '2025-03-14 11:14:57+00', 518, 309);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2166, 5, 3, 144, 'completed', '{"5020": 19153, "5021": 19157, "5022": 19159, "5023": 19162, "5024": 19165, "5025": 19170, "5026": 19171, "5027": 19176}', '2026-05-21 23:55:09+00', '2026-05-21 23:57:33+00', 534, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2167, 7, 1, 272, 'completed', '{"5012": 19129, "5013": 19132, "5014": 19135, "5015": 19138, "5016": 19142, "5017": 19144, "5018": 19147, "5019": 19150}', '2026-03-05 09:23:16+00', '2026-03-05 09:27:48+00', 533, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2168, 1, 0, 26, 'in_progress', '{"4980": 19033}', '2026-01-30 14:15:13+00', '2026-01-30 14:15:24+00', 529, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2169, 7, 1, 248, 'completed', '{"4972": 19009, "4973": 19012, "4974": 19015, "4975": 19018, "4976": 19022, "4977": 19024, "4978": 19027, "4979": 19030}', '2025-03-12 16:54:12+00', '2025-03-12 16:58:20+00', 528, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2170, 3, 5, 304, 'completed', '{"5028": 19178, "5029": 19181, "5030": 19184, "5031": 19186, "5032": 19189, "5033": 19194, "5034": 19197, "5035": 19198}', '2026-03-09 10:56:26+00', '2026-03-09 11:01:30+00', 535, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2171, 1, 1, 40, 'in_progress', '{"4870": 18617, "4873": 18629}', '2025-12-27 06:18:35+00', '2025-12-27 06:19:05+00', 516, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2172, 6, 3, 387, 'completed', '{"4877": 18648, "4878": 18649, "4879": 18654, "4880": 18658, "4881": 18662, "4882": 18668, "4883": 18670, "4884": 18676, "4885": 18677}', '2026-03-31 23:12:55+00', '2026-03-31 23:19:22+00', 517, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2173, 6, 2, 152, 'completed', '{"4996": 19081, "4997": 19084, "4998": 19088, "4999": 19090, "5000": 19093, "5001": 19098, "5002": 19099, "5003": 19102}', '2025-05-23 17:36:54.480531+00', '2025-05-23 17:39:26.480531+00', 531, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2174, 1, 2, 135, 'abandoned', '{"4932": 18865, "4934": 18875, "4935": 18879}', '2026-05-09 08:00:06+00', '2026-05-09 08:01:18+00', 523, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2175, 9, 0, 108, 'completed', '{"4886": 18682, "4887": 18685, "4888": 18689, "4889": 18694, "4890": 18698, "4891": 18702, "4892": 18706, "4893": 18710, "4894": 18714}', '2026-02-25 07:01:52+00', '2026-02-25 07:03:40+00', 518, 310);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2176, 3, 0, 60, 'in_progress', '{"4877": 18646, "4880": 18658, "4883": 18670}', '2025-11-19 02:29:13+00', '2025-11-19 02:30:00+00', 517, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2177, 2, 1, 96, 'abandoned', '{"4862": 18586, "4864": 18596, "4866": 18604}', '2026-03-22 05:21:51.480531+00', '2026-03-22 05:22:26.480531+00', 515, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2178, 2, 0, 84, 'abandoned', '{"5007": 19114, "5011": 19126}', '2025-02-10 08:18:59.480531+00', '2025-02-10 08:19:32.480531+00', 532, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2179, 5, 3, 200, 'completed', '{"4988": 19057, "4989": 19062, "4990": 19063, "4991": 19066, "4992": 19071, "4993": 19073, "4994": 19075, "4995": 19078}', '2026-02-13 20:42:25+00', '2026-02-13 20:45:45+00', 530, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2180, 7, 1, 328, 'completed', '{"4895": 18718, "4896": 18722, "4897": 18726, "4898": 18730, "4899": 18734, "4900": 18738, "4901": 18741, "4902": 18746}', '2026-01-30 23:48:02+00', '2026-01-30 23:53:30+00', 519, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2181, 4, 4, 344, 'completed', '{"4912": 18788, "4913": 18789, "4914": 18794, "4915": 18797, "4916": 18804, "4917": 18805, "4918": 18809, "4919": 18814}', '2025-11-27 19:05:14+00', '2025-11-27 19:10:58+00', 521, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2182, 5, 3, 144, 'completed', '{"5012": 19130, "5013": 19132, "5014": 19137, "5015": 19138, "5016": 19141, "5017": 19144, "5018": 19147, "5019": 19151}', '2026-05-26 21:26:39+00', '2026-05-26 21:29:03+00', 533, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2183, 1, 0, 22, 'abandoned', '{"4932": 18865}', '2024-12-29 19:51:03+00', '2024-12-29 19:51:17+00', 523, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2184, 2, 2, 140, 'abandoned', '{"4903": 18752, "4905": 18760, "4906": 18761, "4909": 18773}', '2024-09-11 16:05:20.480531+00', '2024-09-11 16:06:46.480531+00', 520, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2185, 3, 5, 224, 'completed', '{"4956": 18962, "4957": 18966, "4958": 18967, "4959": 18970, "4960": 18975, "4961": 18976, "4962": 18981, "4963": 18984}', '2025-06-22 00:01:49.480531+00', '2025-06-22 00:05:33.480531+00', 526, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2186, 3, 0, 84, 'abandoned', '{"4938": 18889, "4941": 18901, "4942": 18905}', '2025-12-30 14:30:18.480531+00', '2025-12-30 14:30:48.480531+00', 524, 311);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2187, 2, 7, 396, 'completed', '{"4877": 18646, "4878": 18650, "4879": 18655, "4880": 18659, "4881": 18661, "4882": 18665, "4883": 18669, "4884": 18675, "4885": 18679}', '2026-01-30 04:08:23+00', '2026-01-30 04:14:59+00', 517, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2188, 8, 1, 252, 'completed', '{"4886": 18682, "4887": 18687, "4888": 18689, "4889": 18694, "4890": 18698, "4891": 18702, "4892": 18706, "4893": 18710, "4894": 18714}', '2025-11-18 06:25:38+00', '2025-11-18 06:29:50+00', 518, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2189, 5, 3, 304, 'completed', '{"4972": 19011, "4973": 19014, "4974": 19015, "4975": 19018, "4976": 19022, "4977": 19024, "4978": 19027, "4979": 19030}', '2025-07-14 01:03:53+00', '2025-07-14 01:08:57+00', 528, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2190, 5, 0, 155, 'abandoned', '{"4867": 18606, "4868": 18610, "4870": 18618, "4872": 18625, "4874": 18634}', '2026-02-25 12:21:08+00', '2026-02-25 12:22:07+00', 516, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2191, 2, 1, 63, 'abandoned', '{"5004": 19105, "5009": 19120, "5011": 19127}', '2024-11-23 01:47:20.480531+00', '2024-11-23 01:48:06.480531+00', 532, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2192, 6, 2, 320, 'completed', '{"4920": 18817, "4921": 18822, "4922": 18828, "4923": 18830, "4924": 18833, "4925": 18837, "4926": 18841, "4927": 18846}', '2026-04-15 12:22:57+00', '2026-04-15 12:28:17+00', 522, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2193, 8, 2, 180, 'completed', '{"4946": 18923, "4947": 18926, "4948": 18930, "4949": 18934, "4950": 18938, "4951": 18942, "4952": 18946, "4953": 18950, "4954": 18953, "4955": 18960}', '2026-03-20 14:53:57+00', '2026-03-20 14:56:57+00', 525, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2194, 7, 1, 304, 'completed', '{"4964": 18985, "4965": 18988, "4966": 18991, "4967": 18994, "4968": 18998, "4969": 19000, "4970": 19003, "4971": 19006}', '2025-03-09 20:23:57+00', '2025-03-09 20:29:01+00', 527, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2195, 1, 2, 75, 'in_progress', '{"4903": 18752, "4909": 18776, "4910": 18777}', '2025-03-02 21:14:10.480531+00', '2025-03-02 21:14:57.480531+00', 520, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2196, 4, 0, 84, 'abandoned', '{"4959": 18970, "4960": 18973, "4961": 18976, "4963": 18982}', '2026-05-06 06:09:02.480531+00', '2026-05-06 06:09:20.480531+00', 526, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2197, 2, 6, 232, 'completed', '{"4996": 19081, "4997": 19086, "4998": 19088, "4999": 19090, "5000": 19094, "5001": 19097, "5002": 19100, "5003": 19104}', '2024-08-26 07:53:08.480531+00', '2024-08-26 07:57:00.480531+00', 531, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2198, 0, 5, 160, 'in_progress', '{"4937": 18886, "4939": 18896, "4940": 18898, "4943": 18912, "4945": 18918}', '2025-12-02 16:31:03.480531+00', '2025-12-02 16:32:19.480531+00', 524, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2199, 1, 0, 20, 'abandoned', '{"5022": 19159}', '2026-06-04 10:24:41+00', '2026-06-04 10:24:56+00', 534, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2200, 6, 2, 80, 'completed', '{"4895": 18719, "4896": 18724, "4897": 18726, "4898": 18730, "4899": 18734, "4900": 18738, "4901": 18741, "4902": 18746}', '2025-06-01 11:52:01+00', '2025-06-01 11:53:21+00', 519, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2201, 0, 2, 90, 'in_progress', '{"4928": 18852, "4933": 18871}', '2025-11-24 19:09:10+00', '2025-11-24 19:10:17+00', 523, 312);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2202, 6, 4, 100, 'completed', '{"4936": 18883, "4937": 18888, "4938": 18889, "4939": 18893, "4940": 18898, "4941": 18901, "4942": 18905, "4943": 18909, "4944": 18913, "4945": 18918}', '2025-11-01 03:34:37.480531+00', '2025-11-01 03:36:17.480531+00', 524, 313);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2203, 1, 3, 168, 'abandoned', '{"4895": 18719, "4897": 18725, "4899": 18734, "4902": 18748}', '2024-12-20 04:30:15+00', '2024-12-20 04:31:10+00', 519, 313);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2204, 3, 5, 120, 'completed', '{"4972": 19009, "4973": 19013, "4974": 19017, "4975": 19018, "4976": 19023, "4977": 19025, "4978": 19027, "4979": 19032}', '2025-03-12 01:49:32+00', '2025-03-12 01:51:32+00', 528, 313);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2205, 5, 0, 110, 'abandoned', '{"4869": 18614, "4870": 18618, "4872": 18625, "4873": 18629, "4876": 18642}', '2026-01-20 10:58:44+00', '2026-01-20 10:59:16+00', 516, 313);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2206, 1, 0, 28, 'abandoned', '{"5021": 19156}', '2026-02-23 10:15:24+00', '2026-02-23 10:15:35+00', 534, 313);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2207, 1, 2, 33, 'in_progress', '{"5004": 19106, "5007": 19114, "5011": 19127}', '2025-04-15 07:31:19.480531+00', '2025-04-15 07:31:37.480531+00', 532, 313);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2208, 1, 0, 13, 'abandoned', '{"4984": 19045}', '2026-05-23 15:36:18+00', '2026-05-23 15:36:25+00', 529, 313);
INSERT INTO public.results (id, correct_answers, wrong_answers, time_taken, status, answers, started_at, updated_at, test_id, user_id) VALUES (2209, 0, 0, 28, 'in_progress', '"{\"5057\": 19264, \"5058\": 19267, \"5059\": 19270, \"5060\": 19273}"', '2026-06-16 21:16:38.147232+00', '2026-06-16 21:16:59.000801+00', 539, 314);


--
-- Data for Name: system_configs; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.system_configs (id, key, value, description, created_at, updated_at) VALUES (1, 'mark_in_progress_as_expired_after_days', '120', '', '2026-06-11 15:09:42.654527+00', '2026-06-11 15:09:42.654542+00');


--
-- Data for Name: topics; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (4, 'Matemáticas', 'Cálculo', 'Integrales', true, '2026-06-11 15:00:16.876911+00', '2026-06-11 15:00:16.876923+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (5, 'Matemáticas', 'Geometría', 'Trigonometría', true, '2026-06-11 15:00:16.882728+00', '2026-06-11 15:00:16.882741+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (8, 'Programación', 'Python', 'Clases y objetos', true, '2026-06-11 15:00:16.903332+00', '2026-06-11 15:00:16.903345+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (10, 'Programación', 'JavaScript', 'Async/Await', true, '2026-06-11 15:00:16.918021+00', '2026-06-11 15:00:16.918037+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (12, 'Ciencias', 'Física', 'Termodinámica', true, '2026-06-11 15:00:16.9315+00', '2026-06-11 15:00:16.931511+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (16, 'Historia', 'Historia Antigua', 'Antiguo Egipto', true, '2026-06-11 15:00:16.952645+00', '2026-06-11 15:00:16.952658+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (18, 'Historia', 'Historia Contemporánea', 'Segunda Guerra Mundial', true, '2026-06-11 15:00:16.963288+00', '2026-06-11 15:00:16.963301+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (19, 'Idiomas', 'Inglés', 'Gramática básica', true, '2026-06-11 15:00:16.970122+00', '2026-06-11 15:00:16.970136+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (21, 'Idiomas', 'Español', 'Tiempos verbales', true, '2026-06-11 15:00:16.983963+00', '2026-06-11 15:00:16.983982+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (22, 'Idiomas', 'Francés', 'Conversación básica', true, '2026-06-11 15:00:16.990338+00', '2026-06-11 15:00:16.990351+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (24, 'Tecnología', 'Blockchain', 'Tokens ERC-20', true, '2026-06-11 15:00:17.001189+00', '2026-06-11 15:00:17.001203+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (28, 'Economía', 'Finanzas Personales', 'Inversión básica', true, '2026-06-11 15:00:17.024026+00', '2026-06-11 15:00:17.024038+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (30, 'Economía', 'Mercados Financieros', 'Acciones y bonos', true, '2026-06-11 15:00:17.036058+00', '2026-06-11 15:00:17.036076+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (31, 'Arte', 'Pintura', 'Acuarela', true, '2026-06-11 15:00:17.041668+00', '2026-06-11 15:00:17.041682+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (32, 'Arte', 'Pintura', 'Óleo', true, '2026-06-11 15:00:17.048048+00', '2026-06-11 15:00:17.04807+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (33, 'Arte', 'Dibujo', 'Perspectiva', true, '2026-06-11 15:00:17.054694+00', '2026-06-11 15:00:17.054714+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (34, 'Arte', 'Historia del Arte', 'Renacimiento', true, '2026-06-11 15:00:17.061125+00', '2026-06-11 15:00:17.061138+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (35, 'Música', 'Teoría Musical', 'Escalas musicales', true, '2026-06-11 15:00:17.067351+00', '2026-06-11 15:00:17.067372+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (38, 'Música', 'Piano', 'Lectura de partituras', true, '2026-06-11 15:00:17.086652+00', '2026-06-11 15:00:17.086669+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (39, 'Desarrollo Personal', 'Productividad', 'Gestión del tiempo', true, '2026-06-11 15:00:17.092697+00', '2026-06-11 15:00:17.092711+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (42, 'Desarrollo Personal', 'Liderazgo', 'Trabajo en equipo', true, '2026-06-11 15:00:17.115772+00', '2026-06-11 15:00:17.115796+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (1, 'Matemáticas', 'Álgebra', 'Ecuaciones lineales', false, '2026-06-11 15:00:16.84359+00', '2026-06-16 16:03:10.491771+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (6, 'Programación', 'Python', 'Sintaxis básica', false, '2026-06-11 15:00:16.889353+00', '2026-06-16 16:04:02.953852+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (11, 'Ciencias', 'Física', 'Mecánica clásica', false, '2026-06-11 15:00:16.925922+00', '2026-06-16 16:05:27.801822+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (9, 'Programación', 'JavaScript', 'DOM Manipulation', false, '2026-06-11 15:00:16.910888+00', '2026-06-16 16:06:41.74282+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (15, 'Historia', 'Historia Antigua', 'Imperio Romano', false, '2026-06-11 15:00:16.946928+00', '2026-06-16 16:06:57.698549+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (20, 'Idiomas', 'Inglés', 'Phrasal Verbs', false, '2026-06-11 15:00:16.976926+00', '2026-06-16 16:15:04.749046+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (27, 'Economía', 'Finanzas Personales', 'Presupuestos', false, '2026-06-11 15:00:17.019324+00', '2026-06-16 16:15:18.963707+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (36, 'Música', 'Teoría Musical', 'Acordes', false, '2026-06-11 15:00:17.074042+00', '2026-06-16 16:15:33.379918+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (40, 'Desarrollo Personal', 'Productividad', 'Método Pomodoro', false, '2026-06-11 15:00:17.09834+00', '2026-06-16 16:16:02.705396+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (26, 'Tecnología', 'Ciberseguridad', 'Seguridad de redes', false, '2026-06-11 15:00:17.013095+00', '2026-06-16 16:16:26.266176+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (2, 'Matemáticas', 'Álgebra', 'Ecuaciones cuadráticas', false, '2026-06-11 15:00:16.86437+00', '2026-06-16 16:19:02.80746+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (7, 'Programación', 'Python', 'Funciones', false, '2026-06-11 15:00:16.895992+00', '2026-06-16 16:20:44.086674+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (3, 'Matemáticas', 'Cálculo', 'Derivadas', false, '2026-06-11 15:00:16.871002+00', '2026-06-16 16:20:56.571394+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (17, 'Historia', 'Historia Moderna', 'Revolución Francesa', false, '2026-06-11 15:00:16.95841+00', '2026-06-16 16:21:12.666068+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (14, 'Ciencias', 'Biología', 'Genética', false, '2026-06-11 15:00:16.941857+00', '2026-06-16 16:21:24.438239+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (37, 'Música', 'Guitarra', 'Acordes básicos', false, '2026-06-11 15:00:17.080426+00', '2026-06-16 16:21:36.441147+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (25, 'Tecnología', 'Cloud Computing', 'AWS Fundamentals', false, '2026-06-11 15:00:17.007031+00', '2026-06-16 16:21:47.976761+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (29, 'Economía', 'Macroeconomía', 'Inflación', false, '2026-06-11 15:00:17.029329+00', '2026-06-16 16:21:59.068643+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (41, 'Desarrollo Personal', 'Comunicación', 'Hablar en público', false, '2026-06-11 15:00:17.108436+00', '2026-06-16 16:22:11.938375+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (23, 'Tecnología', 'Blockchain', 'Smart Contracts', false, '2026-06-11 15:00:16.995417+00', '2026-06-16 16:22:23.375664+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (13, 'Ciencias', 'Química', 'Química orgánica', false, '2026-06-11 15:00:16.936887+00', '2026-06-16 21:03:24.78183+00');
INSERT INTO public.topics (id, main_topic, sub_topic, specific_topic, is_predefined, created_at, updated_at) VALUES (46, 'Economía', 'Mercados Financieros', 'Trading', false, '2026-06-18 14:55:09.168921+00', '2026-06-18 14:55:09.168947+00');


--
-- Data for Name: user_quotas; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--

INSERT INTO public.user_quotas (id, month_year, max_requests, used_requests, created_at, updated_at, user_id) VALUES (2, '2026-06', 5, 1, '2026-06-16 21:16:13.02951+00', '2026-06-16 21:16:27.702592+00', 314);
INSERT INTO public.user_quotas (id, month_year, max_requests, used_requests, created_at, updated_at, user_id) VALUES (1, '2026-06', 50, 11, '2026-06-16 20:05:38.262156+00', '2026-06-18 14:52:45.446213+00', 33);


--
-- Data for Name: users_groups; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--



--
-- Data for Name: users_user_permissions; Type: TABLE DATA; Schema: public; Owner: angotest_dj_user
--



--
-- Name: ai_request_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.ai_request_logs_id_seq', 12, true);


--
-- Name: answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.answers_id_seq', 19353, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 68, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 17, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 29, true);


--
-- Name: invitation_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.invitation_events_id_seq', 29, true);


--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.password_reset_tokens_id_seq', 1, false);


--
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.questions_id_seq', 5086, true);


--
-- Name: results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.results_id_seq', 2209, true);


--
-- Name: system_configs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.system_configs_id_seq', 1, true);


--
-- Name: test_invitations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.test_invitations_id_seq', 3, true);


--
-- Name: tests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.tests_id_seq', 540, true);


--
-- Name: topics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.topics_id_seq', 46, true);


--
-- Name: user_quotas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.user_quotas_id_seq', 2, true);


--
-- Name: users_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.users_groups_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.users_id_seq', 314, true);


--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: angotest_dj_user
--

SELECT pg_catalog.setval('public.users_user_permissions_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict 7E0g42tT5CrlvGhop0PHhwkoAeo6zcjdEFRbWfgnyHgVv1uRtnZVJwzJh0h06EV

