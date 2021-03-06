ALTER TABLE "main_app_userprofile" ADD COLUMN "secret_key" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "secret_key" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "user_code" TYPE varchar(30);

ALTER TABLE "main_app_userprofile" DROP COLUMN "user_code" CASCADE;
ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_email" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_email" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_password" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_password" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "token" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "token" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "uid" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "uid" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "user_key" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "user_key" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "secret_key" TYPE varchar(50);

ALTER TABLE "main_app_userprofile" DROP CONSTRAINT "main_app_userp_schema_id_4cddfcbff18e38b1_fk_main_app_schema_id";
ALTER TABLE "main_app_userprofile" DROP COLUMN "schema_id" CASCADE;
DROP TABLE "main_app_schema" CASCADE;

-- Create call teble - 15.10.2015 --
CREATE TABLE "main_app_call" (
	"id" serial NOT NULL PRIMARY KEY,
	"call_id" varchar(30) NOT NULL,
	"sip" varchar(20) NULL,
	"date" timestamp with time zone NULL,
	"destination" varchar(30) NULL,
	"description" varchar(100) NULL,
	"disposition" varchar(20) NULL,
	"bill_seconds" integer NULL,
	"cost" double precision NULL,
	"bill_cost" double precision NULL,
	"currency" varchar(20) NULL,
	"user_profile_id" integer NOT NULL);
ALTER TABLE "main_app_call" ADD CONSTRAINT "main_app_ca_user_profile_id_586a6b3e_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "main_app_call_06037614" ON "main_app_call" ("user_profile_id");

ALTER TABLE "main_app_call" ADD COLUMN "is_answered" boolean DEFAULT true NOT NULL;
ALTER TABLE "main_app_call" ALTER COLUMN "is_answered" DROP DEFAULT;

CREATE TABLE "main_app_callee" ("id" serial NOT NULL PRIMARY KEY, "sip" varchar(20) NOT NULL UNIQUE, "description" varchar(100) NULL, "first_call_date" timestamp with time zone NULL);
ALTER TABLE "main_app_call" DROP COLUMN "description" CASCADE;
ALTER TABLE "main_app_call" DROP COLUMN "sip" CASCADE;
ALTER TABLE "main_app_call" ADD COLUMN "callee_id" integer NOT NULL;
CREATE INDEX "main_app_callee_sip_38a802ef_like" ON "main_app_callee" ("sip" varchar_pattern_ops);
CREATE INDEX "main_app_call_56286df8" ON "main_app_call" ("callee_id");
ALTER TABLE "main_app_call" ADD CONSTRAINT "main_app_call_callee_id_70a0e395_fk_main_app_callee_id" FOREIGN KEY ("callee_id") REFERENCES "main_app_callee" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "main_app_call" ADD COLUMN "record_filename" varchar(100) NULL;
ALTER TABLE "main_app_callee" ALTER COLUMN "description" TYPE varchar(1000);
-- --

-- 30.10.2015 Added Customer number --
ALTER TABLE "main_app_userprofile" ADD COLUMN "customer_number" varchar(10) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "customer_number" DROP DEFAULT;
-- --

-- 02.10.2015 Added SubscribeTransaction, TransactionStatus tables --
CREATE TABLE "main_app_subscribetransaction" ("id" serial NOT NULL PRIMARY KEY, "transact_id" varchar(40) NOT NULL, "receiver" varchar(20) NOT NULL, "form_comments" varchar(50) NULL, "short_dest" varchar(50) NULL, "quickpay_form" varchar(6) NOT NULL, "targets"
varchar(150) NULL, "sum" double precision NOT NULL, "payment_type" varchar(2) NOT NULL, "duration" integer NOT NULL, "expiration_date" timestamp with time zone NULL);
CREATE TABLE "main_app_transactionstatus" ("id" serial NOT NULL PRIMARY KEY, "value" varchar(20) NOT NULL);
ALTER TABLE "main_app_subscribetransaction" ADD COLUMN "status_id" integer NOT NULL;
ALTER TABLE "main_app_subscribetransaction" ALTER COLUMN "status_id" DROP DEFAULT;
ALTER TABLE "main_app_subscribetransaction" ADD COLUMN "user_profile_id" integer NOT NULL;
ALTER TABLE "main_app_subscribetransaction" ALTER COLUMN "user_profile_id" DROP DEFAULT;
CREATE INDEX "main_app_subscribetransaction_dc91ed4b" ON "main_app_subscribetransaction" ("status_id");
ALTER TABLE "main_app_subscribetransaction" ADD CONSTRAINT "main_app_su_status_id_5f99843b_fk_main_app_transactionstatus_id" FOREIGN KEY ("status_id") REFERENCES "main_app_transactionstatus" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "main_app_subscribetransaction_06037614" ON "main_app_subscribetransaction" ("user_profile_id");
ALTER TABLE "main_app_subscribetransaction" ADD CONSTRAINT "main_app_su_user_profile_id_3b9379c6_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "main_app_subscribetransaction" ADD COLUMN "creation_date" timestamp with time zone DEFAULT now() NOT NULL;
ALTER TABLE "main_app_subscribetransaction" ALTER COLUMN "creation_date" DROP DEFAULT;
ALTER TABLE "main_app_subscribetransaction" ADD COLUMN "is_archive" boolean DEFAULT false NOT NULL;
ALTER TABLE "main_app_subscribetransaction" ALTER COLUMN "is_archive" DROP DEFAULT;

ALTER TABLE "main_app_userprofile" ADD COLUMN "date_subscribe_ended" timestamp with time zone NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "date_subscribe_ended" DROP DEFAULT;

ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_phone_number" varchar(20) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_phone_number" DROP DEFAULT;


-- --


-- 19.11.2015 PROFILE REQUEST --
CREATE TABLE "main_app_profilerequesttransaction" ("id" serial NOT NULL PRIMARY KEY, "transact_id" varchar(40) NOT NULL, "creation_date" timestamp with time zone NOT NULL, "email" varchar(30) NOT NULL, "username" varchar(50) NULL, "status_id" integer NOT NULL);

ALTER TABLE "main_app_profilerequesttransaction" ADD CONSTRAINT "main_app_pr_status_id_1cf826c1_fk_main_app_transactionstatus_id" FOREIGN KEY ("status_id") REFERENCES "main_app_transactionstatus" ("id") DEFERRABLE INITIALLY DEFERRED;


-- --

-- 23.12.2015 SIP --

ALTER TABLE "main_app_userprofile" ADD COLUMN "sip" integer NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "sip" DROP DEFAULT;

-- --

-- 30.12.2015 Redirect numbers TABLE --

CREATE TABLE "main_app_redirectnumbers" ("id" serial NOT NULL PRIMARY KEY, "number" varchar(20) NOT NULL, "user_profile_id" integer NOT NULL);
ALTER TABLE "main_app_redirectnumbers" ADD CONSTRAINT "main_app_re_user_profile_id_5ef71571_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "main_app_redirectnumbers_06037614" ON "main_app_redirectnumbers" ("user_profile_id");

ALTER TABLE "main_app_call" DROP COLUMN "is_answered" CASCADE;
ALTER TABLE "main_app_call" ADD COLUMN "call_type" varchar(40) NULL;
ALTER TABLE "main_app_call" ALTER COLUMN "call_type" DROP DEFAULT;

-- --

-- 13.01.16 registered callback table --
-- applying on:
--  work
--  host

CREATE TABLE "main_app_registeredcallback" ("id" serial NOT NULL PRIMARY KEY, "date" timestamp with time zone NOT NULL, "caller" varchar(20) NOT NULL, "destination" varchar(20) NOT NULL, "is_pending" boolean NOT NULL, "user_profile_id" integer NOT NULL);
ALTER TABLE "main_app_registeredcallback" ADD CONSTRAINT "main_app_re_user_profile_id_546c731d_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "main_app_registeredcallback_06037614" ON "main_app_registeredcallback" ("user_profile_id");

-- --

--- INCOMING INFO TABLE , SCRIPT WIDGET TABLE--
-- applying on
-- work
-- home

CREATE TABLE "main_app_incominginfo" ("id" serial NOT NULL PRIMARY KEY, "is_taken" boolean NOT NULL, "caller_id" varchar(30) NOT NULL, "called_did" varchar(30) NOT NULL, "call_start" timestamp with time zone NOT NULL, "expiration_date" timestamp with time zone
NOT NULL);
CREATE TABLE "main_app_widgetscript" ("id" serial NOT NULL PRIMARY KEY, "guid" varchar(40) NOT NULL UNIQUE, "user_profile_id" integer NOT NULL);
ALTER TABLE "main_app_incominginfo" ADD COLUMN "script_id" varchar(40) NOT NULL;
ALTER TABLE "main_app_incominginfo" ALTER COLUMN "script_id" DROP DEFAULT;
ALTER TABLE "main_app_widgetscript" ADD CONSTRAINT "main_app_wid_user_profile_id_913316b_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "main_app_widgetscript_06037614" ON "main_app_widgetscript" ("user_profile_id");
CREATE INDEX "main_app_widgetscript_guid_5aa53910_like" ON "main_app_widgetscript" ("guid" varchar_pattern_ops);
CREATE INDEX "main_app_incominginfo_a19ff0c0" ON "main_app_incominginfo" ("script_id");
ALTER TABLE "main_app_incominginfo" ADD CONSTRAINT "main_app_incom_script_id_26c86eea_fk_main_app_widgetscript_guid" FOREIGN KEY ("script_id") REFERENCES "main_app_widgetscript" ("guid") DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE "main_app_widgetscript" DROP CONSTRAINT "main_app_wid_user_profile_id_913316b_fk_main_app_userprofile_id";
ALTER TABLE "main_app_widgetscript" ADD CONSTRAINT "main_app_widgetscript_user_profile_id_913316b_uniq" UNIQUE ("user_profile_id");
ALTER TABLE "main_app_widgetscript" ADD CONSTRAINT "main_app_wid_user_profile_id_913316b_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;


-- --


ALTER TABLE "main_app_incominginfo" DROP COLUMN "is_taken" CASCADE;
ALTER TABLE "main_app_incominginfo" ADD COLUMN "guid" varchar(40) DEFAULT '' NOT NULL UNIQUE;
ALTER TABLE "main_app_incominginfo" ALTER COLUMN "guid" DROP DEFAULT;


ALTER TABLE "main_app_callee" ADD COLUMN "user_profile_id" integer NOT NULL;
ALTER TABLE "main_app_callee" ALTER COLUMN "user_profile_id" DROP DEFAULT;
ALTER TABLE "main_app_callee" DROP CONSTRAINT "main_app_callee_sip_key";
CREATE INDEX "main_app_callee_06037614" ON "main_app_callee" ("user_profile_id");
ALTER TABLE "main_app_callee" ADD CONSTRAINT "main_app_ca_user_profile_id_7306109e_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;
