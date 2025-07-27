CREATE TABLE tbl_ref(
    id SERIAL PRIMARY KEY,
    namespace VARCHAR(256),
    key VARCHAR(20),
    value JSONB
);
CREATE INDEX idx_ref_ns_lower ON tbl_ref (lower(namespace));
CREATE INDEX idx_ref_key_lower ON tbl_ref (lower(namespace),lower(key));
COMMENT ON TABLE tbl_ref IS '参数设置表';
COMMENT ON COLUMN tbl_ref.namespace IS 'like <table-device.column-type>';
COMMENT ON COLUMN tbl_ref.key IS 'like <CCT-40B>';
COMMENT ON COLUMN tbl_ref.value IS 'like <"{"value":[{"zh-cn":"半自动智能炒菜机"},{"en-us":“Semi-auto Smart Wok”}]}">';