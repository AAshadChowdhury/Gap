USE [dbTrade]
GO
/****** Object:  StoredProcedure [dbo].[prcGetGapData]    Script Date: 5/12/2022 10:00:21 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
--	Exec prcGetGapData 'TWTR', '01-Jan-2012', '31-Dec-2022'
ALTER proc [dbo].[prcGetGapData] @SymName varchar(15), @dtFrom varchar(30), @dtTo varchar(30), @TF varchar(30)='History Data (Daily)'
as
	Select symName, dtDate, [open], [high], [low], [close], Isnull(GapStatus,'') gapStatus,
	DATEDIFF(s,'01-Jan-1970',dtDate) * convert(bigint, 1000) [time]
	from tblHistoryData
	Where SymName = @SymName
		and dtDate Between @dtFrom and @dtTo
		and TimeFrame = @TF

Go
sp_help prcGetGapData
go
sp_help tblHistoryData