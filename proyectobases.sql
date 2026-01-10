--
-- PostgreSQL database dump
--

\restrict 6DnF1KPpXYFaON0xFhi6HQlxUrLho6xOlw5ofDKvFzzQAiCXoRyeFcViEUOe65c

-- Dumped from database version 17.6 (Debian 17.6-1.pgdg13+1)
-- Dumped by pg_dump version 17.6

-- Started on 2026-01-05 05:33:30

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 16407)
-- Name: cliente; Type: TABLE; Schema: public; Owner: Fish72
--

CREATE TABLE public.cliente (
    id_usuario integer NOT NULL,
    fecha_registro date NOT NULL,
    tipo_cliente character varying(30)
);


ALTER TABLE public.cliente OWNER TO "Fish72";

--
-- TOC entry 232 (class 1259 OID 16485)
-- Name: consumo_servicio; Type: TABLE; Schema: public; Owner: Fish72
--

CREATE TABLE public.consumo_servicio (
    id_consumo integer NOT NULL,
    id_reserva integer NOT NULL,
    id_servicio integer NOT NULL,
    cantidad integer,
    subtotal numeric(10,2),
    CONSTRAINT consumo_servicio_cantidad_check CHECK ((cantidad > 0)),
    CONSTRAINT consumo_servicio_subtotal_check CHECK ((subtotal >= (0)::numeric))
);


ALTER TABLE public.consumo_servicio OWNER TO "Fish72";

--
-- TOC entry 231 (class 1259 OID 16484)
-- Name: consumo_servicio_id_consumo_seq; Type: SEQUENCE; Schema: public; Owner: Fish72
--

CREATE SEQUENCE public.consumo_servicio_id_consumo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.consumo_servicio_id_consumo_seq OWNER TO "Fish72";

--
-- TOC entry 3512 (class 0 OID 0)
-- Dependencies: 231
-- Name: consumo_servicio_id_consumo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Fish72
--

ALTER SEQUENCE public.consumo_servicio_id_consumo_seq OWNED BY public.consumo_servicio.id_consumo;


--
-- TOC entry 222 (class 1259 OID 16417)
-- Name: empleado; Type: TABLE; Schema: public; Owner: Fish72
--

CREATE TABLE public.empleado (
    id_usuario integer NOT NULL,
    fecha_contratacion date NOT NULL,
    salario numeric(10,2),
    id_rol integer NOT NULL,
    CONSTRAINT empleado_salario_check CHECK ((salario >= (0)::numeric))
);


ALTER TABLE public.empleado OWNER TO "Fish72";

--
-- TOC entry 224 (class 1259 OID 16434)
-- Name: habitacion; Type: TABLE; Schema: public; Owner: Fish72
--

CREATE TABLE public.habitacion (
    id_habitacion integer NOT NULL,
    numero integer NOT NULL,
    tipo character varying(50) NOT NULL,
    precio_noche numeric(10,2),
    estado character varying(30) NOT NULL,
    CONSTRAINT habitacion_precio_noche_check CHECK ((precio_noche > (0)::numeric))
);


ALTER TABLE public.habitacion OWNER TO "Fish72";

--
-- TOC entry 223 (class 1259 OID 16433)
-- Name: habitacion_id_habitacion_seq; Type: SEQUENCE; Schema: public; Owner: Fish72
--

CREATE SEQUENCE public.habitacion_id_habitacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.habitacion_id_habitacion_seq OWNER TO "Fish72";

--
-- TOC entry 3513 (class 0 OID 0)
-- Dependencies: 223
-- Name: habitacion_id_habitacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Fish72
--

ALTER SEQUENCE public.habitacion_id_habitacion_seq OWNED BY public.habitacion.id_habitacion;


--
-- TOC entry 230 (class 1259 OID 16472)
-- Name: pago; Type: TABLE; Schema: public; Owner: Fish72
--

CREATE TABLE public.pago (
    id_pago integer NOT NULL,
    fecha_pago date NOT NULL,
    monto numeric(10,2),
    metodo_pago character varying(50),
    estado_pago character varying(30),
    id_reserva integer NOT NULL,
    CONSTRAINT pago_monto_check CHECK ((monto > (0)::numeric))
);


ALTER TABLE public.pago OWNER TO "Fish72";

--
-- TOC entry 229 (class 1259 OID 16471)
-- Name: pago_id_pago_seq; Type: SEQUENCE; Schema: public; Owner: Fish72
--

CREATE SEQUENCE public.pago_id_pago_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pago_id_pago_seq OWNER TO "Fish72";

--
-- TOC entry 3514 (class 0 OID 0)
-- Dependencies: 229
-- Name: pago_id_pago_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Fish72
--

ALTER SEQUENCE public.pago_id_pago_seq OWNED BY public.pago.id_pago;


--
-- TOC entry 226 (class 1259 OID 16444)
-- Name: reserva; Type: TABLE; Schema: public; Owner: Fish72
--

CREATE TABLE public.reserva (
    id_reserva integer NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    estado character varying(30) NOT NULL,
    id_cliente integer NOT NULL,
    id_habitacion integer NOT NULL,
    CONSTRAINT chk_fechas CHECK ((fecha_fin > fecha_inicio))
);


ALTER TABLE public.reserva OWNER TO "Fish72";

--
-- TOC entry 225 (class 1259 OID 16443)
-- Name: reserva_id_reserva_seq; Type: SEQUENCE; Schema: public; Owner: Fish72
--

CREATE SEQUENCE public.reserva_id_reserva_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reserva_id_reserva_seq OWNER TO "Fish72";

--
-- TOC entry 3515 (class 0 OID 0)
-- Dependencies: 225
-- Name: reserva_id_reserva_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Fish72
--

ALTER SEQUENCE public.reserva_id_reserva_seq OWNED BY public.reserva.id_reserva;


--
-- TOC entry 220 (class 1259 OID 16399)
-- Name: rol_empleado; Type: TABLE; Schema: public; Owner: Fish72
--

CREATE TABLE public.rol_empleado (
    id_rol integer NOT NULL,
    nombre_rol character varying(50) NOT NULL
);


ALTER TABLE public.rol_empleado OWNER TO "Fish72";

--
-- TOC entry 219 (class 1259 OID 16398)
-- Name: rol_empleado_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: Fish72
--

CREATE SEQUENCE public.rol_empleado_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rol_empleado_id_rol_seq OWNER TO "Fish72";

--
-- TOC entry 3516 (class 0 OID 0)
-- Dependencies: 219
-- Name: rol_empleado_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Fish72
--

ALTER SEQUENCE public.rol_empleado_id_rol_seq OWNED BY public.rol_empleado.id_rol;


--
-- TOC entry 228 (class 1259 OID 16462)
-- Name: servicio; Type: TABLE; Schema: public; Owner: Fish72
--

CREATE TABLE public.servicio (
    id_servicio integer NOT NULL,
    nombre character varying(100) NOT NULL,
    precio numeric(10,2),
    CONSTRAINT servicio_precio_check CHECK ((precio >= (0)::numeric))
);


ALTER TABLE public.servicio OWNER TO "Fish72";

--
-- TOC entry 227 (class 1259 OID 16461)
-- Name: servicio_id_servicio_seq; Type: SEQUENCE; Schema: public; Owner: Fish72
--

CREATE SEQUENCE public.servicio_id_servicio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.servicio_id_servicio_seq OWNER TO "Fish72";

--
-- TOC entry 3517 (class 0 OID 0)
-- Dependencies: 227
-- Name: servicio_id_servicio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Fish72
--

ALTER SEQUENCE public.servicio_id_servicio_seq OWNED BY public.servicio.id_servicio;


--
-- TOC entry 218 (class 1259 OID 16390)
-- Name: usuario; Type: TABLE; Schema: public; Owner: Fish72
--

CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    nombre character varying(100) NOT NULL,
    correo character varying(100) NOT NULL,
    contrasena_hash character varying(255) NOT NULL,
    telefono character varying(20)
);


ALTER TABLE public.usuario OWNER TO "Fish72";

--
-- TOC entry 217 (class 1259 OID 16389)
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: Fish72
--

CREATE SEQUENCE public.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_usuario_seq OWNER TO "Fish72";

--
-- TOC entry 3518 (class 0 OID 0)
-- Dependencies: 217
-- Name: usuario_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Fish72
--

ALTER SEQUENCE public.usuario_id_usuario_seq OWNED BY public.usuario.id_usuario;


--
-- TOC entry 3318 (class 2604 OID 16488)
-- Name: consumo_servicio id_consumo; Type: DEFAULT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.consumo_servicio ALTER COLUMN id_consumo SET DEFAULT nextval('public.consumo_servicio_id_consumo_seq'::regclass);


--
-- TOC entry 3314 (class 2604 OID 16437)
-- Name: habitacion id_habitacion; Type: DEFAULT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.habitacion ALTER COLUMN id_habitacion SET DEFAULT nextval('public.habitacion_id_habitacion_seq'::regclass);


--
-- TOC entry 3317 (class 2604 OID 16475)
-- Name: pago id_pago; Type: DEFAULT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.pago ALTER COLUMN id_pago SET DEFAULT nextval('public.pago_id_pago_seq'::regclass);


--
-- TOC entry 3315 (class 2604 OID 16447)
-- Name: reserva id_reserva; Type: DEFAULT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.reserva ALTER COLUMN id_reserva SET DEFAULT nextval('public.reserva_id_reserva_seq'::regclass);


--
-- TOC entry 3313 (class 2604 OID 16402)
-- Name: rol_empleado id_rol; Type: DEFAULT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.rol_empleado ALTER COLUMN id_rol SET DEFAULT nextval('public.rol_empleado_id_rol_seq'::regclass);


--
-- TOC entry 3316 (class 2604 OID 16465)
-- Name: servicio id_servicio; Type: DEFAULT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.servicio ALTER COLUMN id_servicio SET DEFAULT nextval('public.servicio_id_servicio_seq'::regclass);


--
-- TOC entry 3312 (class 2604 OID 16393)
-- Name: usuario id_usuario; Type: DEFAULT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuario_id_usuario_seq'::regclass);


--
-- TOC entry 3335 (class 2606 OID 16411)
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 3351 (class 2606 OID 16492)
-- Name: consumo_servicio consumo_servicio_pkey; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.consumo_servicio
    ADD CONSTRAINT consumo_servicio_pkey PRIMARY KEY (id_consumo);


--
-- TOC entry 3337 (class 2606 OID 16422)
-- Name: empleado empleado_pkey; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.empleado
    ADD CONSTRAINT empleado_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 3339 (class 2606 OID 16442)
-- Name: habitacion habitacion_numero_key; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.habitacion
    ADD CONSTRAINT habitacion_numero_key UNIQUE (numero);


--
-- TOC entry 3341 (class 2606 OID 16440)
-- Name: habitacion habitacion_pkey; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.habitacion
    ADD CONSTRAINT habitacion_pkey PRIMARY KEY (id_habitacion);


--
-- TOC entry 3349 (class 2606 OID 16478)
-- Name: pago pago_pkey; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_pkey PRIMARY KEY (id_pago);


--
-- TOC entry 3343 (class 2606 OID 16450)
-- Name: reserva reserva_pkey; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_pkey PRIMARY KEY (id_reserva);


--
-- TOC entry 3331 (class 2606 OID 16406)
-- Name: rol_empleado rol_empleado_nombre_rol_key; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.rol_empleado
    ADD CONSTRAINT rol_empleado_nombre_rol_key UNIQUE (nombre_rol);


--
-- TOC entry 3333 (class 2606 OID 16404)
-- Name: rol_empleado rol_empleado_pkey; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.rol_empleado
    ADD CONSTRAINT rol_empleado_pkey PRIMARY KEY (id_rol);


--
-- TOC entry 3345 (class 2606 OID 16470)
-- Name: servicio servicio_nombre_key; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.servicio
    ADD CONSTRAINT servicio_nombre_key UNIQUE (nombre);


--
-- TOC entry 3347 (class 2606 OID 16468)
-- Name: servicio servicio_pkey; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.servicio
    ADD CONSTRAINT servicio_pkey PRIMARY KEY (id_servicio);


--
-- TOC entry 3353 (class 2606 OID 16494)
-- Name: consumo_servicio uq_reserva_servicio; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.consumo_servicio
    ADD CONSTRAINT uq_reserva_servicio UNIQUE (id_reserva, id_servicio);


--
-- TOC entry 3327 (class 2606 OID 16397)
-- Name: usuario usuario_correo_key; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_correo_key UNIQUE (correo);


--
-- TOC entry 3329 (class 2606 OID 16395)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 3354 (class 2606 OID 16412)
-- Name: cliente fk_cliente_usuario; Type: FK CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT fk_cliente_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3360 (class 2606 OID 16495)
-- Name: consumo_servicio fk_consumo_reserva; Type: FK CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.consumo_servicio
    ADD CONSTRAINT fk_consumo_reserva FOREIGN KEY (id_reserva) REFERENCES public.reserva(id_reserva) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3361 (class 2606 OID 16500)
-- Name: consumo_servicio fk_consumo_servicio; Type: FK CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.consumo_servicio
    ADD CONSTRAINT fk_consumo_servicio FOREIGN KEY (id_servicio) REFERENCES public.servicio(id_servicio) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3355 (class 2606 OID 16428)
-- Name: empleado fk_empleado_rol; Type: FK CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.empleado
    ADD CONSTRAINT fk_empleado_rol FOREIGN KEY (id_rol) REFERENCES public.rol_empleado(id_rol) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3356 (class 2606 OID 16423)
-- Name: empleado fk_empleado_usuario; Type: FK CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.empleado
    ADD CONSTRAINT fk_empleado_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3359 (class 2606 OID 16479)
-- Name: pago fk_pago_reserva; Type: FK CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT fk_pago_reserva FOREIGN KEY (id_reserva) REFERENCES public.reserva(id_reserva) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3357 (class 2606 OID 16451)
-- Name: reserva fk_reserva_cliente; Type: FK CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT fk_reserva_cliente FOREIGN KEY (id_cliente) REFERENCES public.cliente(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3358 (class 2606 OID 16456)
-- Name: reserva fk_reserva_habitacion; Type: FK CONSTRAINT; Schema: public; Owner: Fish72
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT fk_reserva_habitacion FOREIGN KEY (id_habitacion) REFERENCES public.habitacion(id_habitacion) ON UPDATE CASCADE ON DELETE RESTRICT;


-- Completed on 2026-01-05 05:33:30

--
-- PostgreSQL database dump complete
--

\unrestrict 6DnF1KPpXYFaON0xFhi6HQlxUrLho6xOlw5ofDKvFzzQAiCXoRyeFcViEUOe65c

