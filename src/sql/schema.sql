--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.4
-- Dumped by pg_dump version 9.4.0
-- Started on 2015-09-22 11:48:29

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 179 (class 3079 OID 11855)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2044 (class 0 OID 0)
-- Dependencies: 179
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 175 (class 1259 OID 57379)
-- Name: author; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE author (
    aid integer NOT NULL,
    name text
);


ALTER TABLE author OWNER TO "postgres";

--
-- TOC entry 178 (class 1259 OID 57397)
-- Name: contains; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE contains (
    cid integer NOT NULL,
    paper_id integer,
    keyword_id integer
);


ALTER TABLE contains OWNER TO "postgres";

--
-- TOC entry 173 (class 1259 OID 57363)
-- Name: keyword; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE keyword (
    kid integer NOT NULL,
    value text
);


ALTER TABLE keyword OWNER TO "postgres";

--
-- TOC entry 172 (class 1259 OID 57355)
-- Name: paper; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE paper (
    pid integer NOT NULL,
    title text,
    year integer,
    venue_id integer
);


ALTER TABLE paper OWNER TO "postgres";

--
-- TOC entry 176 (class 1259 OID 57387)
-- Name: refs; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE refs (
    rid integer NOT NULL,
    from_id integer,
    to_id integer
);


ALTER TABLE refs OWNER TO "postgres";

--
-- TOC entry 174 (class 1259 OID 57371)
-- Name: venue; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE venue (
    vid integer NOT NULL,
    name text
);


ALTER TABLE venue OWNER TO "postgres";

--
-- TOC entry 177 (class 1259 OID 57392)
-- Name: writes; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE writes (
    wid integer NOT NULL,
    paper_id integer,
    author_id integer
);


ALTER TABLE writes OWNER TO "postgres";

--
-- TOC entry 2033 (class 0 OID 57379)
-- Dependencies: 175
-- Data for Name: author; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY author (aid, name) FROM stdin;
\.


--
-- TOC entry 2036 (class 0 OID 57397)
-- Dependencies: 178
-- Data for Name: contains; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY contains (cid, paper_id, keyword_id) FROM stdin;
\.


--
-- TOC entry 2031 (class 0 OID 57363)
-- Dependencies: 173
-- Data for Name: keyword; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY keyword (kid, value) FROM stdin;
\.


--
-- TOC entry 2030 (class 0 OID 57355)
-- Dependencies: 172
-- Data for Name: paper; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY paper (pid, title, year, venue_id) FROM stdin;
\.


--
-- TOC entry 2034 (class 0 OID 57387)
-- Dependencies: 176
-- Data for Name: refs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY refs (rid, from_id, to_id) FROM stdin;
\.


--
-- TOC entry 2032 (class 0 OID 57371)
-- Dependencies: 174
-- Data for Name: venue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY venue (vid, name) FROM stdin;
\.


--
-- TOC entry 2035 (class 0 OID 57392)
-- Dependencies: 177
-- Data for Name: writes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY writes (wid, paper_id, author_id) FROM stdin;
\.


--
-- TOC entry 1914 (class 2606 OID 57386)
-- Name: aid; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY author
    ADD CONSTRAINT aid PRIMARY KEY (aid);


--
-- TOC entry 1920 (class 2606 OID 57401)
-- Name: cid; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contains
    ADD CONSTRAINT cid PRIMARY KEY (cid);


--
-- TOC entry 1910 (class 2606 OID 57370)
-- Name: kid; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY keyword
    ADD CONSTRAINT kid PRIMARY KEY (kid);


--
-- TOC entry 1908 (class 2606 OID 57362)
-- Name: pid; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY paper
    ADD CONSTRAINT pid PRIMARY KEY (pid);


--
-- TOC entry 1916 (class 2606 OID 57391)
-- Name: rid; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY refs
    ADD CONSTRAINT rid PRIMARY KEY (rid);


--
-- TOC entry 1912 (class 2606 OID 57378)
-- Name: vid; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY venue
    ADD CONSTRAINT vid PRIMARY KEY (vid);


--
-- TOC entry 1918 (class 2606 OID 57396)
-- Name: wid; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY writes
    ADD CONSTRAINT wid PRIMARY KEY (wid);


--
-- TOC entry 2043 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM "postgres";
GRANT ALL ON SCHEMA public TO "postgres";
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-09-22 11:48:29

--
-- PostgreSQL database dump complete
--

