use dbTrade
go
drop procedure  if exists spGetGapUpDown
go


CREATE PROCEDURE spGetGapUpDown @SymName varchar(15), @dtDate varchar(30) , @TimeFrame varchar(30)
AS begin
With CTE
as
(
	Select dtDate, [open], [high], [low], [close], volume, vwap, symName, 
		Case 
			When [low]> Lag([high],1) Over(Partition By SymName order by dtDate) Then 
				Case when [low] - Lag([high],1) Over(Partition By SymName order by dtDate)>0 then [low] - Lag([high],1) Over(Partition By SymName order by dtDate) else 0 end
		End 'GapUp'
		,Case 
			When [low]> Lag([high],1) Over(Partition By SymName order by dtDate) Then 
				Case when [Low]/Lag([high],1) Over(Partition By SymName order by dtDate)>1.03 then [Low]/Lag([high],1) Over(Partition By SymName order by dtDate) else 0 end
		End 'GapUpPer'
		,
		Case 
			When Lag([low],1) Over(Partition By SymName order by dtDate)> [high]  Then 
				Case when Lag([low],1) Over(Partition By SymName order by dtDate) - [high]>0 then Lag([low],1) Over(Partition By SymName order by dtDate) - [high] else 0 end
		End 'GapDown'
		,
		Case 
			When Lag([low],1) Over(Partition By SymName order by dtDate)> [high]  Then 
				Case when Lag([low],1) Over(Partition By SymName order by dtDate)/[high]>1.02 then Lag([low],1) Over(Partition By SymName order by dtDate)/[high] else 0 end
		End 'GapDownPer'
		--,	Case When Lag([close],1) Over(order by dtDate)-[close] > 0 then 'Bear' else 'Bull' End 'Trend'
	from tblHistoryData
	Where 
		SymName = @SymName
		and 
		TimeFrame= @TimeFrame
		 and dtDate > @dtDate
) 
Select *
from CTE
Where-- GapUp !=0
       --or GapDown !=0
	--and Gap_Percent >1.03
	--and
	SymName = 'TWTR'
Order By SymName, dtDate
end

Go
exec spGetGapUpDown @SymName='TWTR',@dtDate='01-Jan-2022',  @TimeFrame='History Data (Daily)'
Go

--sp_help tblHistoryData

select * from tblBacktest
