-- =============================================
-- ATM CASH LOGISTICS DATABASE SETUP
-- =============================================
USE master;
GO

-- 1. Create Database (If it doesn't exist)
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'ATMLogisticsDB')
BEGIN
    CREATE DATABASE ATMLogisticsDB;
END
GO

USE ATMLogisticsDB;
GO

-- 2. Create Master Table: Fixed ATM Locations
IF OBJECT_ID('Ref_ATM_Locations', 'U') IS NULL
BEGIN
    CREATE TABLE Ref_ATM_Locations (
        ATMID INT PRIMARY KEY,              -- Unique ID (e.g., 1001)
        ATMName VARCHAR(100),               -- e.g., "Kenyatta Ave Branch"
        Region VARCHAR(50),                 -- e.g., "CBD"
        Latitude DECIMAL(9, 6),             -- GPS Y
        Longitude DECIMAL(9, 6),            -- GPS X
        MaxCapacity DECIMAL(18, 2) DEFAULT 5000000 -- Max Cash (5M KES)
    );
END
GO

-- 3. Create Inventory Table: Live Cash Levels
IF OBJECT_ID('Live_Cash_Inventory', 'U') IS NULL
BEGIN
    CREATE TABLE Live_Cash_Inventory (
        InventoryID BIGINT IDENTITY(1,1) PRIMARY KEY,
        ATMID INT REFERENCES Ref_ATM_Locations(ATMID),
        CurrentBalance DECIMAL(18, 2),
        CashLevelPercentage DECIMAL(5, 2), -- (Current / Max) * 100
        Status VARCHAR(20),                -- 'Online', 'Critical', etc.
        LastUpdated DATETIME DEFAULT GETDATE()
    );
END
GO

-- 4. Create Logistics View (The "Brain" for Power BI)
-- This view joins location data with live inventory and determines "Action Needed"
CREATE OR ALTER VIEW v_ATM_Fleet_Status AS
SELECT 
    L.ATMID,
    L.ATMName,
    L.Latitude,
    L.Longitude,
    L.Region,
    I.CurrentBalance,
    I.CashLevelPercentage,
    I.Status,
    -- Business Logic for Heat Map
    CASE 
        WHEN I.CashLevelPercentage < 20 THEN 'Critical Alert' -- Red
        WHEN I.CashLevelPercentage < 40 THEN 'Refill Needed'  -- Orange
        ELSE 'Healthy'                                        -- Green
    END AS LogisticsAction
FROM Ref_ATM_Locations L
JOIN Live_Cash_Inventory I ON L.ATMID = I.ATMID;
GO

PRINT 'Database, Tables, and Views created successfully.';