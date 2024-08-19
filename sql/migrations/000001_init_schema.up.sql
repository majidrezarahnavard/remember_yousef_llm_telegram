--liquibase formatted sql
-- changeset sarina:1

CREATE TABLE IF NOT EXISTS "faqs" (
  "id" bigserial PRIMARY KEY,
  "user_id" TEXT NOT NULL,
  "question" TEXT NOT NULL,
  "answer" TEXT NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT (now())
);

CREATE INDEX ON "faqs" ("id");
--rollback DROP TABLE "faqs";
