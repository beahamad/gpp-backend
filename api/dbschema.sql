CREATE TABLE public.phone (
    id integer NOT NULL,
    imei character varying(15) NOT NULL,
    number1 character varying(20) NOT NULL,
    number2 character varying(20) NOT NULL,
    is_lost boolean DEFAULT false,
    user_id integer NOT NULL,
    model character varying(255)
);

CREATE SEQUENCE public.phone_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.phone_id_seq OWNED BY public.phone.id;

CREATE TABLE public."user" (
    id integer NOT NULL,
    cpf character varying(11) NOT NULL,
    full_name character varying(100) NOT NULL,
    date_of_birth date NOT NULL,
    address character varying(200) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(100) NOT NULL,
    confirmation_code character varying(4),
    confirmed boolean DEFAULT false,
    ispolicia boolean
);

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;

ALTER TABLE ONLY public.phone ALTER COLUMN id SET DEFAULT nextval('public.phone_id_seq'::regclass);

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);

COPY public."user" (id, cpf, full_name, date_of_birth, address, email, password, confirmation_code, confirmed, ispolicia) FROM stdin;

SELECT pg_catalog.setval('public.phone_id_seq', 60, true);

SELECT pg_catalog.setval('public.user_id_seq', 8, true);

ALTER TABLE ONLY public.phone
    ADD CONSTRAINT phone_imei_key UNIQUE (imei);

ALTER TABLE ONLY public.phone
    ADD CONSTRAINT phone_number1_key UNIQUE (number1);

ALTER TABLE ONLY public.phone
    ADD CONSTRAINT phone_number2_key UNIQUE (number2);

ALTER TABLE ONLY public.phone
    ADD CONSTRAINT phone_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_cpf_key UNIQUE (cpf);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.phone
    ADD CONSTRAINT phone_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);
