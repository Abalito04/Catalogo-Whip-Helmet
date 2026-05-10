--
-- PostgreSQL database dump
--

\restrict 4t4jHxkLF9N1cLmWYWpvrlRVkhhFMSrnjIQXZyXsOk9Jy1a6q5ucpZtLhyZSWpf

-- Dumped from database version 17.7 (Debian 17.7-3.pgdg13+1)
-- Dumped by pg_dump version 18.3

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

--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_stat_statements IS 'track planning and execution statistics of all SQL statements executed';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cascos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cascos (
    id integer NOT NULL,
    nombre_modelo character varying(100) NOT NULL,
    marca character varying(50) NOT NULL,
    tipo character varying(20),
    condicion character varying(10) NOT NULL,
    precio double precision NOT NULL,
    descripcion text,
    talle character varying(10),
    color character varying(30),
    imagen_principal character varying(200),
    imagenes_adicionales text,
    instagram_url character varying(300),
    disponible boolean,
    destacado boolean,
    fecha_agregado timestamp without time zone,
    reservado boolean DEFAULT false,
    precio_1_cuota double precision,
    precio_3_cuotas double precision,
    precio_6_cuotas double precision
);


ALTER TABLE public.cascos OWNER TO postgres;

--
-- Name: cascos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cascos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cascos_id_seq OWNER TO postgres;

--
-- Name: cascos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cascos_id_seq OWNED BY public.cascos.id;


--
-- Name: items_pedido; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.items_pedido (
    id integer NOT NULL,
    pedido_id integer NOT NULL,
    casco_id integer NOT NULL,
    precio double precision NOT NULL
);


ALTER TABLE public.items_pedido OWNER TO postgres;

--
-- Name: items_pedido_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.items_pedido_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.items_pedido_id_seq OWNER TO postgres;

--
-- Name: items_pedido_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.items_pedido_id_seq OWNED BY public.items_pedido.id;


--
-- Name: pedidos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pedidos (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    dni character varying(20) NOT NULL,
    telefono character varying(30) NOT NULL,
    email character varying(100),
    tipo_entrega character varying(10) NOT NULL,
    codigo_postal character varying(10),
    provincia character varying(100),
    ciudad character varying(100),
    direccion character varying(200),
    metodo_pago character varying(30),
    estado character varying(20),
    mp_payment_id character varying(100),
    total double precision NOT NULL,
    fecha timestamp without time zone
);


ALTER TABLE public.pedidos OWNER TO postgres;

--
-- Name: pedidos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pedidos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pedidos_id_seq OWNER TO postgres;

--
-- Name: pedidos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pedidos_id_seq OWNED BY public.pedidos.id;


--
-- Name: cascos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cascos ALTER COLUMN id SET DEFAULT nextval('public.cascos_id_seq'::regclass);


--
-- Name: items_pedido id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items_pedido ALTER COLUMN id SET DEFAULT nextval('public.items_pedido_id_seq'::regclass);


--
-- Name: pedidos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos ALTER COLUMN id SET DEFAULT nextval('public.pedidos_id_seq'::regclass);


--
-- Data for Name: cascos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cascos (id, nombre_modelo, marca, tipo, condicion, precio, descripcion, talle, color, imagen_principal, imagenes_adicionales, instagram_url, disponible, destacado, fecha_agregado, reservado, precio_1_cuota, precio_3_cuotas, precio_6_cuotas) FROM stdin;
4	F2	Fly Racing	Motocross	usado	1	Casco Fly Racing F2 \r\nCarbono/kevlar\r\nTalle M.\r\nImpecable estado.	M		https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609545/whip-helmets/ewwrl0t6a4yqarv69tuz.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609546/whip-helmets/kyjhj0yg57mqfhqjimky.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609547/whip-helmets/byqdkysmomkhvdy4a8s1.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609547/whip-helmets/a3undisc4fxzths1kmkx.png	https://www.instagram.com/p/DQMcn7SEViW	f	f	2026-01-11 01:49:44.639732	f	\N	\N	\N
21	GP	Troy Lee Designs 100%	Motocross	usado	1	Casco Troy Lee Designs GP\r\nTalle L\r\nImpecable estado.	L	Azul	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769606195/whip-helmets/tgcfohy4eytl6g8kmnzg.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769606195/whip-helmets/gcouh9tmp4rr3hdmqwii.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769606196/whip-helmets/i5fzaqmc75d2m99yjn5i.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769606197/whip-helmets/z2nyxszlcvnmszma4f28.png	https://www.instagram.com/p/DUBDdmFjXTH	f	f	2026-01-28 13:16:38.47213	f	\N	\N	\N
5	V1	Fox	Motocross	usado	320000	Casco Fox V1\r\nTalle S\r\nMuy buen estado	S	Azul	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608199/whip-helmets/ijw4zkcbjbyg03kjrfw3.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608200/whip-helmets/thgqflliksu5zevekcmg.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608200/whip-helmets/s8sxulj8ewb9qqdq2fzv.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608201/whip-helmets/xlwcdfmudbcgqzmfbglh.png	https://www.instagram.com/p/DRKSwTHjZtb	t	f	2026-01-11 01:49:44.639732	f	417373.16	\N	\N
10	GP	Troy Lee Designs 	Motocross	usado	340000	Casco Troy Lee Designs GP\r\nTalle XL\r\nMuy buen estado.	XL	Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608612/whip-helmets/acvphii987tij0dkww0q.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608613/whip-helmets/bxpjizvadut76lasls4b.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608614/whip-helmets/t1upwtweh72b3mywbghd.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608615/whip-helmets/touur8v99qs16apkw55l.png	https://www.instagram.com/p/DO6EgAPjT7W	t	f	2026-01-11 01:49:44.639732	f	443458.98	\N	\N
1	SM5	Alpinestars	Motocross	usado	395000	Casco Alpinestars SM5 \r\nTalle M\r\nMuy buen estado	M	Negro y Rojo	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609382/whip-helmets/egvxmwrgmcvnmlen5oxf.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609382/whip-helmets/usj02afblf8bzq8dt7vb.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609383/whip-helmets/onbsdlnepw4sc38v9c5a.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609383/whip-helmets/gjen9hhkgmr3se26lydw.png	https://www.instagram.com/p/DRCcAVRDfc4	f	f	2026-01-11 01:49:44.639732	f	515194.99	\N	\N
18	V1	Fox	Motocross	usado	335000	Casco Fox V1\r\nTalle S\r\nMuy buen estado.	S	Blanco y Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608013/whip-helmets/zrv1dwxivnnpfnopwaop.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1768655554/whip-helmets/yojopu7r2mdpeh58cbta.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608015/whip-helmets/uxea9tr2ikv4rsoojxne.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608015/whip-helmets/pupbvslxzp1zgte8euft.png	https://www.instagram.com/p/DTfgDTBjTE7	t	f	2026-01-17 13:12:35.364118	f	436937.52	\N	\N
20	D4 Carbono	Troy Lee Designs 100%	DH/BMX	usado	1	Casco Troy Lee Designs D4 carbono\r\nTalle L\r\nImpecable estado.\r\nPara DH/bmx.	L	Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769606064/whip-helmets/q7utm8c2pesm8cwaenxt.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769606064/whip-helmets/mfpa50irxfhztafvqmso.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769606065/whip-helmets/ot6pj8xbcgry93ht3fky.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769606065/whip-helmets/mmymznqclkic5mwwxpcc.png	https://www.instagram.com/p/DT-drEDjVON	f	f	2026-01-28 13:14:26.324985	f	\N	\N	\N
24	VFX-W Block-Pass	Shoei		usado	1	Casco Shoei vfx-w block-pass\r\nTalle L\r\nMuy buen estado.	L	Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609843/whip-helmets/hnufgeegsagsupljiuyk.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609844/whip-helmets/r55htl6zanwfzftj2pqf.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609845/whip-helmets/neikouzfdm4xordcqlr4.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609846/whip-helmets/w0rsg35f21ias37cgjm1.png	https://www.instagram.com/p/DTngJkWjQod	f	f	2026-01-28 14:17:27.115604	f	\N	\N	\N
16	SE4 GP Pinstripe-Carbono	Troy Lee Designs 100%	Motocross	usado	1	Casco Troy Lee Designs 100% SE4 Pinstripe.\r\nCarbono.\r\nTalle M\r\nMuy buen estado.	M	Negro y Dorado	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609085/whip-helmets/aeaypq1fsj5jxiykybyk.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609085/whip-helmets/fwhv4lambg6pgz7px6ta.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609086/whip-helmets/hkxmkx8dnl6hwyfr4m54.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609087/whip-helmets/xx7wzsg8mx7ks4wkh5y3.png	https://www.instagram.com/p/DSKpGF0jTjf	f	f	2026-01-11 01:49:44.639732	f	\N	\N	\N
2	Moto-9 Flex Carbono	Bell	Motocross	usado	1	Casco Bell Moto-9 Flex carbono \r\nTalle L.\r\nBuen estado.	L	Blanco y Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609216/whip-helmets/m5kbcpepmnlvocot255u.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609217/whip-helmets/yiriypvmw5ov8k5ya0kl.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609218/whip-helmets/enljf3ads1cl1ul79g1w.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609219/whip-helmets/q8jncqrmmlkox78epqtj.png	https://www.instagram.com/p/DOJLVWPjegD	f	f	2026-01-11 01:49:44.639732	f	\N	\N	\N
3	Mx-9-Monster	Bell	Motocross	usado	1	Casco Bell Mx-9 monster pro circuit.\r\nTalle M.\r\nBuen estado.	M	Negro y Verde	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609470/whip-helmets/e8eiyxt4ywc54oc9doma.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609471/whip-helmets/dkn18keo8siincy1iid9.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609471/whip-helmets/mcpnq0alh3ymnzdvloiq.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609472/whip-helmets/ye9trpsliam95w6b2pow.png	https://www.instagram.com/p/DOyUjwdjS-Q	f	f	2026-01-11 01:49:44.639732	f	\N	\N	\N
13	MX-9- Mips Fasthouse	Bell	Motocross	usado	1	Casco Bell Moto 9 Mips Fasthouse\r\nTalle S\r\nMuy buen estado, con bolso.	S	Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608894/whip-helmets/cvtnmp6pdfp4oqtvkxsi.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608895/whip-helmets/meohdceo71ajxdvino6b.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608896/whip-helmets/bmt2ht6uqnux5zbwhner.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608896/whip-helmets/stujo9nckiqm2bt5xbw2.png	https://www.instagram.com/p/DRj-6JvjaCa	f	f	2026-01-11 01:49:44.639732	f	\N	\N	\N
9	GP	Troy Lee Designs 	Motocross	nuevo	455000	Troy Lee Designs GP\r\nTalles L\r\nNuevos en caja.	L	Negro y Blanco	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608526/whip-helmets/wttpbqwlyjhhtegsxluy.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608527/whip-helmets/mhv6votgfuzlk6zk55pp.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608527/whip-helmets/ax8fgb2lotzqqjqdhksc.png	https://www.instagram.com/p/DQKAHj5kTVb	t	t	2026-01-11 01:49:44.639732	f	593452.46	\N	\N
8	D4	Troy Lee Designs 100%	Motocross	usado	350000	Casco Troy Lee Designs 100% D4\r\nTalle M.\r\nMuy buen estado.\r\nMips y tornillos de repuesto.	M	Azul	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609317/whip-helmets/jeyp8ysaabiryrsfvl8e.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609318/whip-helmets/auh74yb4esxgk8ey8crh.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609318/whip-helmets/fulttbm1jn7qgne3impf.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609319/whip-helmets/pwyhwrvzjieyvzr8z13l.png	https://www.instagram.com/p/DG1kVvpNAZY	t	f	2026-01-11 01:49:44.639732	f	456501.89	\N	\N
12	SM5	Alpinestars	Motocross	usado	395000	Casco Alpinestars SM5 \r\nTalle M\r\nMuy buen estado.\r\n	M	Negro, Rojo y Celeste	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608799/whip-helmets/evo4lqx8mwcnsc85oruz.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608800/whip-helmets/wgvuuivprk3jsvpyghxb.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608800/whip-helmets/dcptmmfvwxeyoywy01xb.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608801/whip-helmets/eztwkuskdgre0dpkqszn.png	https://www.instagram.com/p/DR2CZYDDbfP	t	f	2026-01-11 01:49:44.639732	f	515194.99	\N	\N
11	Switch Spacer	Airoh	Motocross	usado	175000	Casco Airoh Switch Spacer\r\nTalle XS\r\nBuen estado.	XS	Negro y Naranja	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608726/whip-helmets/ris0hkvpunnfswolald9.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608726/whip-helmets/fvhcyzsb6jsomhqmpsxy.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608727/whip-helmets/hvqh8mvafkazwihyfspt.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608728/whip-helmets/rwgdyd8kkyflsxgjduv3.png	https://www.instagram.com/p/DSC8NCSDT1P	t	f	2026-01-11 01:49:44.639732	f	228250.95	\N	\N
22	Moto 9 Flex Edición Tagger	Bell	Motocross	usado	455000	Casco Bell moto 9 Flex edición tagger \r\nTalle M\r\nImpecable estado.	M	Celeste	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609677/whip-helmets/lubk5jchp9xcvl8zsg2o.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609678/whip-helmets/ql6vspaheo1l3oqyjybr.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609680/whip-helmets/cauxndeayv0q12jtfegm.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609681/whip-helmets/onldzybotyjqbm6kzo47.png	https://www.instagram.com/p/DTdDm1FDclB	f	f	2026-01-28 14:14:42.309368	f	593452.46	\N	\N
15	V3-Motif	Fox	Motocross	nuevo	465000	Casco Fox V3 motif \r\nTalle M\r\nNuevo.	M	Gris y Azul	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609021/whip-helmets/mgdvietz8rlca7bifeet.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609021/whip-helmets/vvdw268k0n6yo7at8ise.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609022/whip-helmets/vxrvvvvnfmtxg1j8c4zl.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609023/whip-helmets/ip1nlqeqbypzcd3ufqe1.png	https://www.instagram.com/p/DSupBPMDajo	f	f	2026-01-11 01:49:44.639732	f	606495.37	\N	\N
17	SE5 Carbono	Troy Lee Designs 	Motocross	usado	759700	Casco Troy Lee Designs  SE5 Carbono\r\nTalle M\r\nImpecable estado.\r\nCon bolso y visera.	M	Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609153/whip-helmets/qfy1nhhufhbidxkvmc8s.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609154/whip-helmets/qg7vkrt9tlmnz4du8b74.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609155/whip-helmets/jrjkttnpc4bcxo2q6ntu.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609155/whip-helmets/jnlveyuch1l0jzgffpej.png	https://www.instagram.com/p/DRzbabwDa1I	t	f	2026-01-11 01:49:44.639732	f	990869.96	\N	\N
23	VFX-W Capacitor	Shoei		usado	1	Casco Shoei vfx-w capacitor\r\nTalle L\r\nImpecable estado.	L	Azul	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609768/whip-helmets/htgj2nr4s3b2eg8dqwl5.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609768/whip-helmets/stcqb3g3lbroeadwqwol.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609769/whip-helmets/q3dht0ajddi3nitgeath.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609770/whip-helmets/ave6hdweoip7qmdtbndr.png	https://www.instagram.com/p/DTiJ12QDdvk	f	f	2026-01-28 14:16:11.86255	f	\N	\N	\N
6	V3-RS Ghost	Fox	Motocross	usado	1	Casco Fox V3 RS Carbon Solid \r\nTalle M\r\nIgual a nuevo, con bolso, interior de repuesto y 3 viseras.\r\n	M	Ghost Edition	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608327/whip-helmets/z9z4kofirsfl4lnnpfxu.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608328/whip-helmets/vszcwmi9qtt5xuytztgn.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608329/whip-helmets/hpwbpsre9hlsx7fhnpsj.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608329/whip-helmets/wzv53sffmvdwt4m3mlsi.png	https://www.instagram.com/p/DQo4WVvjTYn	f	f	2026-01-11 01:49:44.639732	f	\N	\N	\N
25	SM5	Alpinestars		usado	395000	Casco Alpinestars SM5\r\nTalle M\r\nImpecable estado.	M	Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609909/whip-helmets/v0d0hwaquw6xtsxpxrdh.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609910/whip-helmets/ylrmngwegxqi9ubcp6gx.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609911/whip-helmets/zjjz9t3kqggn0h1ryjgh.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769609912/whip-helmets/wrgawekykkysffgjpdpv.png	https://www.instagram.com/p/DTkuXnSDTM9	t	f	2026-01-28 14:18:33.387829	f	515194.99	\N	\N
29	Fórmula Cp Rush	Fly Racing	Motocross	nuevo	305000	Casco Fly Racing Fórmula Cp rush\r\nTalle YL (52/53cm)\r\nNuevo.\r\n	YL	Rojo, Blanco y Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979739/whip-helmets/dekavubfl91qyw9ihz7d.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979746/whip-helmets/xs1luxzfa5c1t3zps7jn.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979752/whip-helmets/if8vzwpwxin97j1s6hah.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979760/whip-helmets/gqjklaqcm2or9lt8lzmq.png	https://www.instagram.com/p/DUYTujQEcPI	t	t	2026-03-08 14:22:40.897838	f	397808.79	\N	\N
26	SM5	Alpinestars	Motocross	usado	395000	Casco Alpinestars SM5\r\nTalle M\r\nImpecable estado.	M	Negro y Amarillo	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772952204/whip-helmets/d9jzksfdwhvg1wv7eggj.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772952753/whip-helmets/sspqxqnhg6hr4fps928s.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1772952755/whip-helmets/siokuhjftk8a5qjbxpwc.png	https://www.instagram.com/p/DUnsQJeDVO5	t	f	2026-03-08 06:37:34.275534	f	515194.99	\N	\N
28	ATR-2 Alpha	6D	Motocross	usado	540000	Casco 6D ATR-2 alpha\r\nTalle M\r\nImpecable estado.	M	Negro y Amarillo	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979535/whip-helmets/donbefnallsg67m9s4ag.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979544/whip-helmets/jglx3frw8yxvisjlgce0.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979552/whip-helmets/bqmqw6so6ixv11pkkvej.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979559/whip-helmets/onmipjtwztgn45gnj7qc.png	https://www.instagram.com/p/DVbNW_mDVc3	f	f	2026-03-08 14:19:19.693353	f	704315.98	\N	\N
27	V1	Fox	Motocross	usado	1	Casco Fox V1\r\nTalle S\r\nIgual a nuevo.	S	Negro y Rojo	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979342/whip-helmets/a0ddczyxsfc2giqyz3zk.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979343/whip-helmets/ups08msc1ttn0okyudvd.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979343/whip-helmets/hfhuisvidqmeeatk1tuo.png	https://www.instagram.com/p/DQhEzqljS-b	f	f	2026-03-08 14:15:44.340219	f	\N	\N	\N
7	V3-Moth LE Copper	Fox	Motocross	usado	210000	Casco Fox V3 Moth LE Copper\r\nTalle S\r\nBuen estado.	S	Copper Limited Edition	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608394/whip-helmets/vv4rltrcphgcr7jv7kkw.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608394/whip-helmets/sr3c7talztyswbvmnjn1.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608396/whip-helmets/yaxyepyhokrazhu9jv1n.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608399/whip-helmets/zsquurd2wmfr3brpo99v.png	https://www.instagram.com/p/DMd93LCgyBo	t	f	2026-01-11 01:49:44.639732	f	273901.13	\N	\N
31	GP	Troy Lee Designs 	Motocross	usado	355000	Casco Troy Lee Designs GP\r\nTalle YL 53/54cm\r\nMuy buen estado.	YL	Negro 	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772980181/whip-helmets/zba2oqlilxrzu7jyybnx.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772980189/whip-helmets/vjnjl0gh5egjvtorpbcq.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1772980197/whip-helmets/pk1bdeyw9vs1lmtixprh.png	https://www.instagram.com/p/DUs9gqMjbrJ	t	f	2026-03-08 14:29:58.13043	f	463023.35	\N	\N
19	SE4 	Troy Lee Designs 	Motocross	usado	340000	Casco Troy Lee Designs SE4\r\nTalle XL\r\nIgual a nuevo.	XL	Blanco y Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608087/whip-helmets/ngjjxysqhbtfdgcstppm.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1769605933/whip-helmets/lew8mvmndlod8bzzb2ey.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769605935/whip-helmets/pxs9h8iaysrh906x3y3p.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1769608087/whip-helmets/ymg04f9l3zkem6gujwep.png	https://www.instagram.com/p/DT5dC42jTW6	t	f	2026-01-28 13:12:15.517293	f	443458.98	\N	\N
30	Moto 10 Fasthouse	Bell	Motocross	usado	951400	Casco Bell Moto 10 Fasthouse\r\nTalle M\r\nMuy buen estado	M	Blanco y Negro	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979920/whip-helmets/jzi9m0r88jcc8rtq4shd.png	https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979928/whip-helmets/gjs2v7bpvdpqrsjzm33n.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979934/whip-helmets/fy6bhke60rwjm81upvxl.png,https://res.cloudinary.com/ddowcuhlu/image/upload/v1772979943/whip-helmets/fvb6rawpsiyvc6knrbu1.png	https://www.instagram.com/p/DUivFCQjVSj	t	t	2026-03-08 14:25:44.336595	f	1240902.57	\N	\N
\.


--
-- Data for Name: items_pedido; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.items_pedido (id, pedido_id, casco_id, precio) FROM stdin;
\.


--
-- Data for Name: pedidos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pedidos (id, nombre, apellido, dni, telefono, email, tipo_entrega, codigo_postal, provincia, ciudad, direccion, metodo_pago, estado, mp_payment_id, total, fecha) FROM stdin;
\.


--
-- Name: cascos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cascos_id_seq', 34, true);


--
-- Name: items_pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.items_pedido_id_seq', 2, true);


--
-- Name: pedidos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pedidos_id_seq', 2, true);


--
-- Name: cascos cascos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cascos
    ADD CONSTRAINT cascos_pkey PRIMARY KEY (id);


--
-- Name: items_pedido items_pedido_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items_pedido
    ADD CONSTRAINT items_pedido_pkey PRIMARY KEY (id);


--
-- Name: pedidos pedidos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_pkey PRIMARY KEY (id);


--
-- Name: items_pedido items_pedido_casco_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items_pedido
    ADD CONSTRAINT items_pedido_casco_id_fkey FOREIGN KEY (casco_id) REFERENCES public.cascos(id);


--
-- Name: items_pedido items_pedido_pedido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items_pedido
    ADD CONSTRAINT items_pedido_pedido_id_fkey FOREIGN KEY (pedido_id) REFERENCES public.pedidos(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 4t4jHxkLF9N1cLmWYWpvrlRVkhhFMSrnjIQXZyXsOk9Jy1a6q5ucpZtLhyZSWpf

