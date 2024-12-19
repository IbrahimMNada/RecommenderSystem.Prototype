BEGIN TRANSACTION;
GO

CREATE INDEX [IX_Users_Status_Dates] ON [Users] ([Status], [ActivationDate], [CreatedAt]);
GO

CREATE INDEX [IX_Surveys_Status_Dates] ON [Surveys] ([Status], [EndDate], [StartDate]);
GO

CREATE INDEX [IX_RTOIRequests_Status_CreatedAt] ON [RTOIRequests] ([Status], [CreatedAt]);
GO

CREATE INDEX [IX_Consultations_Status_Dates] ON [Consultations] ([ConsultationStatus], [EndDate], [StartDate]);
GO

INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
VALUES (N'20241218140506_Adding-indexers', N'7.0.11');
GO

COMMIT;
GO

ALTER PROCEDURE [dbo].[ConsultationEndDateProcedure] 
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @CurrentDate DATETIME = GETDATE();

    IF EXISTS (
        SELECT 1
        FROM dbo.Consultations
        WHERE ConsultationStatus <> 6
          AND DATEADD(day, 1, EndDate) < @CurrentDate
    )
    BEGIN
        UPDATE dbo.Consultations
        SET ConsultationStatus = 6
        WHERE ConsultationStatus <> 6
          AND DATEADD(day, 1, EndDate) < @CurrentDate;
    END


    IF EXISTS (
        SELECT 1
        FROM dbo.Surveys
        WHERE [Status] <> 6
          AND DATEADD(day, 1, EndDate) < @CurrentDate
    )
    BEGIN
        UPDATE dbo.Surveys
        SET [Status] = 6
        WHERE [Status] <> 6
          AND DATEADD(day, 1, EndDate) < @CurrentDate;
    END


    IF EXISTS (
        SELECT 1
        FROM dbo.Users
        WHERE Status <> 4
          AND Status = 1
          AND DATEDIFF(day, ISNULL(ActivationDate, CreatedAt), @CurrentDate) > 2
    )
    BEGIN
        UPDATE dbo.Users
        SET Status = 4
        WHERE Status <> 4
          AND Status = 1
          AND DATEDIFF(day, ISNULL(ActivationDate, CreatedAt), @CurrentDate) > 2;
    END


    IF EXISTS (
        SELECT 1
        FROM dbo.Consultations
        WHERE ConsultationStatus <> 5
          AND ConsultationStatus = 4
          AND StartDate <= @CurrentDate
          AND EndDate > @CurrentDate
    )
    BEGIN
        UPDATE dbo.Consultations
        SET ConsultationStatus = 5
        WHERE ConsultationStatus <> 5
          AND ConsultationStatus = 4
          AND StartDate <= @CurrentDate
          AND EndDate > @CurrentDate;
    END


    IF EXISTS (
        SELECT 1
        FROM dbo.Surveys
        WHERE [Status] <> 5
          AND [Status] = 4
          AND StartDate <= @CurrentDate
          AND EndDate > @CurrentDate
    )
    BEGIN
        UPDATE dbo.Surveys
        SET [Status] = 5
        WHERE [Status] <> 5
          AND [Status] = 4
          AND StartDate <= @CurrentDate
          AND EndDate > @CurrentDate;
    END


    IF EXISTS (
        SELECT 1
        FROM dbo.RTOIRequests
        WHERE LateValidation <> 1
          AND Status = 1
          AND DATEDIFF(day, CreatedAt, @CurrentDate) > 33
    )
    BEGIN
        UPDATE dbo.RTOIRequests
        SET LateValidation = 1
        WHERE LateValidation <> 1
          AND Status = 1
          AND DATEDIFF(day, CreatedAt, @CurrentDate) > 33;
    END

    RETURN 1;
END
