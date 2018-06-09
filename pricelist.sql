
/****** Object:  View [dbo].[ostatki]    Script Date: 06/09/2018 10:28:44 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/*
Поля выгрузки

--код товара 
-- наименование
-- производитель 
-- страна
-- остаток в текущей единице
-- розничная цена с НДС
-- внутренний ШК партии
-- ШК товара заводской
--- наименование склада
--- ЖВ препарат или не очень
-- срок годности
-- серия 
---- цена производителя без НДС
-- цена поставщика  
-- НДС поставщика Рубли
---ставка НДС поставщика 
--- ставка НДС розничная
-- ндс розничная (Рубли)
-- зарегистрированная цена если есть (без ндс)
-- ндс пост
-- Единица делитель
-- Единица делимое
--- серитфикат





select ID_STORE, NAME from STORE    ---- список складов



select count( *) from lot
where (dbo.LOT.QUANTITY_REM > 0) 
 проверка по количеству партий -все выгрузилось или нет*/
CREATE VIEW [dbo].[ostatki]
AS
SELECT     TOP (100) PERCENT dbo.LOT.ID_GOODS, dbo.GOODS.NAME, dbo.PRODUCER.NAME AS prod_name, dbo.COUNTRY.NAME AS cnt_name, dbo.LOT.QUANTITY_REM, 
                      dbo.LOT.PRICE_SAL, dbo.LOT.INTERNAL_BARCODE,
                          (SELECT     TOP (1) CODE
                            FROM          dbo.BAR_CODE
                            WHERE      (ID_GOODS = dbo.LOT.ID_GOODS) AND (DATE_DELETED IS NULL)) AS EXTERNAL_BARCODE, dbo.STORE.NAME AS Sklad, dbo.GOODS.IMPORTANT, 
                      dbo.SERIES.BEST_BEFORE, dbo.SERIES.SERIES_NUMBER, dbo.LOT.PRICE_PROD, dbo.LOT.PRICE_SUP, dbo.LOT.PVAT_SUP, dbo.LOT.VAT_SUP, dbo.LOT.VAT_SAL, 
                      dbo.LOT.PVAT_SAL, dbo.LOT.REGISTER_PRICE, dbo.LOT.VAT_SUP AS Expr1, dbo.SCALING_RATIO.DENOMINATOR, dbo.SCALING_RATIO.NUMERATOR, 
                      dbo.REG_CERT.NAME AS Cert
FROM         dbo.LOT INNER JOIN
                      dbo.GOODS ON dbo.LOT.ID_GOODS = dbo.GOODS.ID_GOODS INNER JOIN
                      dbo.PRODUCER ON dbo.GOODS.ID_PRODUCER = dbo.PRODUCER.ID_PRODUCER INNER JOIN
                      dbo.STORE ON dbo.LOT.ID_STORE = dbo.STORE.ID_STORE INNER JOIN
                      dbo.SCALING_RATIO ON dbo.LOT.ID_SCALING_RATIO = dbo.SCALING_RATIO.ID_SCALING_RATIO AND 
                      dbo.GOODS.ID_GOODS = dbo.SCALING_RATIO.ID_GOODS LEFT OUTER JOIN
                      dbo.SERIES ON dbo.LOT.ID_SERIES = dbo.SERIES.ID_SERIES AND dbo.GOODS.ID_GOODS = dbo.SERIES.ID_GOODS LEFT OUTER JOIN
                      dbo.REG_CERT ON dbo.LOT.ID_REG_CERT_GLOBAL = dbo.REG_CERT.ID_REG_CERT_GLOBAL LEFT OUTER JOIN
                      dbo.COUNTRY ON dbo.PRODUCER.ID_COUNTRY = dbo.COUNTRY.ID_COUNTRY
WHERE     (dbo.LOT.QUANTITY_REM > 0)
ORDER BY dbo.GOODS.NAME

GO
