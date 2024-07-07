INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff,
                              is_active, date_joined)
VALUES (1, 'pbkdf2_sha256$600000$hMTLEJUldZmSjlMExNwcs0$//+sFoS/XusF2QdYY81vUr+dIo768LW5pA9ZGi6kXeA=', null, true,
        'django', '', '', 'django@test.com', true, true, '2024-07-07 09:13:18.796402 +00:00');

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);
