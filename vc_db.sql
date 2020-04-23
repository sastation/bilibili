-- Initial script to create new table

ALTER TABLE bbvc RENAME TO bbvc01;

CREATE TABLE IF NOT EXISTS bbvc (
    bvid vchar(25) primary key, 
    avnum vchar(25), 
    uploadtime vchar(10),
    playnum integer, 
    dmnum integer, 
    palacetime vchar(10),
    v_reply integer,
    v_favorite integer,
    updatetime vchar(10),
    v_coin integer,
    v_share integer,
    downtime vchar(10),
    downstatus vchar(5),
    title vchar(255)
);

INSERT INTO bbvc (
    bvid, avnum, uploadtime, playnum, dmnum, palacetime, updatetime, downtime, downstatus, title)
SELECT bvid, avnum, uploadtime, playnum, dmnum, palacetime, updatetime, downtime, downstatus, title
FROM bbvc01;
