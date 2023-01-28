using System.Collections.Generic;
using System.Linq;
using BitMexLibrary;

namespace MachinaTrader.Indicators
{

	public static partial class Extensions
	{
		public static List<decimal?> PivotHigh(this List<Candle> source, int barsLeft = 4, int barsRight = 2, bool fillNullValues = false)
		{
			var result = new List<decimal?>();
            
			for (int i = 0; i < source.Count; i++)
			{
				if (i < barsLeft + barsRight)
				{
					result.Add(null);
					continue;
				}
                
				var isPivot = true;
				var subSet = source.Skip(i - barsLeft - barsRight).Take(barsLeft + barsRight + 1).ToList();
				var valueToCheck = subSet[barsLeft];

				// Check if the [barsLeft] bars left of what we're checking all have lower highs or equal
				for (int leftPivot = 0; leftPivot < barsLeft; leftPivot++)
				{
					if (subSet[leftPivot].High > valueToCheck.High)
					{
						isPivot = false;
						break;
					}
				}
