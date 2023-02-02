// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © sbyegon

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © sbyegon

//@version=5
indicator(title="Divergence Indicator Update", format=format.price)
len = input.int(title="RSI Period", minval=1, defval=14)
src = input(title="RSI Source", defval=close)
lbR = input(title="Pivot Lookback Right", defval=5)
lbL = input(title="Pivot Lookback Left", defval=5)
rangeUpper = input(title="Max of Lookback Range", defval=60)
rangeLower = input(title="Min of Lookback Range", defval=5)
plotBull = input(title="Plot Bullish", defval=true)
plotHiddenBull = input(title="Plot Hidden Bullish", defval=false)
plotBear = input(title="Plot Bearish", defval=true)
plotHiddenBear = input(title="Plot Hidden Bearish", defval=false)
bearColor = color.red
bullColor = color.green
hiddenBullColor = color.new(color.green, 80)
hiddenBearColor = color.new(color.red, 80)
textColor = color.white
noneColor = color.new(color.white, 100)
osc = ta.rsi(src, len)

plot(osc, title="RSI", linewidth=2, color=#2962FF)
hline(50, title="Middle Line", color=#787B86, linestyle=hline.style_dotted)
obLevel = hline(70, title="Overbought", color=#787B86, linestyle=hline.style_dotted)
osLevel = hline(30, title="Oversold", color=#787B86, linestyle=hline.style_dotted)
fill(obLevel, osLevel, title="Background", color=color.rgb(33, 150, 243, 90))

//

//
pls = ta.pivotlow(osc, lbL, lbR)
phs = ta.pivothigh(osc, lbL, lbR) 
plFound = na(pls) ? false : true
phFound = na(phs) ? false : true
_inRange(cond) =>
	bars = ta.barssince(cond == true)
	rangeLower <= bars and bars <= rangeUpper

// Logging in Pinescript
log_show      = input(true, title = "Show Log?",               group = "Log")
log_show_msg  = input(10,   title = "# of message to show",    group = "Log")
log_offset    = input.int(0,    title = "# of messages to offset", group = "Log", step = 1)

// LOGGING FUNCTION ///

var bar_arr  = array.new_int(0)
var time_arr = array.new_string(0)
var msg_arr  = array.new_string(0)
var type_arr = array.new_string(0)

log_msg(message, type) => 
    array.push(bar_arr,  bar_index)
    array.push(time_arr, str.tostring(year) + "-" + str.tostring(month) + "-" + str.tostring(dayofmonth) + " " + str.tostring(hour) + ":" + str.tostring(minute) + ":" + str.tostring(second))
    array.push(msg_arr,  message)
    array.push(type_arr, type)	


hprice = 0.0
hprice :=  not na(phs) ? phs : hprice[1]

lprice = 0.0
lprice := not na(pls) ? pls : lprice[1]

plot(hprice, color = color.green, linewidth = 2)
plot(lprice, color = color.red,   linewidth = 2)

// Pivot Points Messages //

if (not na(phs))
    log_msg("New Pivot High phs: " + str.tostring(hprice), 'message')

if (not na(phs) and hprice > hprice[1])
    log_msg("New Pivot Higher High phs: " + str.tostring(hprice), 'warning')



if (not na(pls))
    log_msg("New Pivot Low pls: " + str.tostring(lprice), 'message')

rt = ta.valuewhen(plFound, osc[lbR], 1)
pt  = osc[lbR] 

if (not na(pls) and lprice < lprice[1])
    log_msg("New Pivot Lower Low pls2: " + str.tostring(lprice), 'warning')
	log_msg("RSI Value when PL happens: " + str.tostring(rt), 'warning')
	log_msg("PlFound: " + str.tostring(plFound), 'warning')
	log_msg("PlFound 1: " + str.tostring(plFound[1]), 'warning')
	log_msg("Sixth recent RSI Value: " + str.tostring(pt), 'warning')



//a = ta.valuewhen(plFound, osc[lbR], 1)
//b = int(a)
//plot(a, color = color.green, style = plot.style_stepline_diamond) // linewidth = 2, 
//label.new(b,  osc, style = label.style_circle, text="rsi value =" + str.tostring(a) )
//plotchar(a, char = "a")
//plot(plFound, color = color.red,   linewidth = 2)
//------------------------------------------------------------------------------
// Regular Bullish
// Osc: Higher Low

oscHL = osc[lbR] > ta.valuewhen(plFound, osc[lbR], 1) and _inRange(plFound[1])
// Price: Lower Low

priceLL = low[lbR] < ta.valuewhen(plFound, low[lbR], 1)
bullCond = plotBull and priceLL and oscHL and plFound

if (bullCond)
    log_msg("Regular Bullish Divergence !!", 'error')

plot(
     plFound ? osc[lbR] : na,
     offset=-lbR,
     title="Regular Bullish",
     linewidth=2,
     color=(bullCond ? bullColor : noneColor)
     )

plotshape(
	 bullCond ? osc[lbR] : na,
	 offset=-lbR,
	 title="Regular Bullish Label",
	 text=" Bull ",
	 style=shape.labelup,
	 location=location.absolute,
	 color=bullColor,
	 textcolor=textColor
	 )

//------------------------------------------------------------------------------
// Hidden Bullish
// Osc: Lower Low

oscLL = osc[lbR] < ta.valuewhen(plFound, osc[lbR], 1) and _inRange(plFound[1])

// Price: Higher Low

priceHL = low[lbR] > ta.valuewhen(plFound, low[lbR], 1)
hiddenBullCond = plotHiddenBull and priceHL and oscLL and plFound

plot(
	 plFound ? osc[lbR] : na,
	 offset=-lbR,
	 title="Hidden Bullish",
	 linewidth=2,
	 color=(hiddenBullCond ? hiddenBullColor : noneColor)
	 )

plotshape(
	 hiddenBullCond ? osc[lbR] : na,
	 offset=-lbR,
	 title="Hidden Bullish Label",
	 text=" H Bull ",
	 style=shape.labelup,
	 location=location.absolute,
	 color=bullColor,
	 textcolor=textColor
	 )

//------------------------------------------------------------------------------
// Regular Bearish
// Osc: Lower High

oscLH = osc[lbR] < ta.valuewhen(phFound, osc[lbR], 1) and _inRange(phFound[1])

// Price: Higher High

priceHH = high[lbR] > ta.valuewhen(phFound, high[lbR], 1)

bearCond = plotBear and priceHH and oscLH and phFound
if (bearCond)
    log_msg("Regular Bearish Divergence !!", 'error')	

plot(
	 phFound ? osc[lbR] : na,
	 offset=-lbR,
	 title="Regular Bearish",
	 linewidth=2,
	 color=(bearCond ? bearColor : noneColor)
	 )

plotshape(
	 bearCond ? osc[lbR] : na,
	 offset=-lbR,
	 title="Regular Bearish Label",
	 text=" Bear ",
	 style=shape.labeldown,
	 location=location.absolute,
	 color=bearColor,
	 textcolor=textColor
	 )

//------------------------------------------------------------------------------
// Hidden Bearish
// Osc: Higher High

oscHH = osc[lbR] > ta.valuewhen(phFound, osc[lbR], 1) and _inRange(phFound[1])

// Price: Lower High

priceLH = high[lbR] < ta.valuewhen(phFound, high[lbR], 1)

hiddenBearCond = plotHiddenBear and priceLH and oscHH and phFound

plot(
	 phFound ? osc[lbR] : na,
	 offset=-lbR,
	 title="Hidden Bearish",
	 linewidth=2,
	 color=(hiddenBearCond ? hiddenBearColor : noneColor)
	 )

plotshape(
	 hiddenBearCond ? osc[lbR] : na,
	 offset=-lbR,
	 title="Hidden Bearish Label",
	 text=" H Bear ",
	 style=shape.labeldown,
	 location=location.absolute,

        table.cell(log_tbl, 2, i, array.get(msg_arr, arr_i),           bgcolor = msg_color, text_size = size.small)
	 color=bearColor,
	 textcolor=textColor
	 )

///////////////////////////////
// Create and fill log table //

var log_tbl = table.new(position.bottom_left, 3, log_show_msg + 1, border_width = 1)

if (barstate.islast and log_show)
    
    table.cell(log_tbl, 0, 0, "Bar #",   bgcolor = color.gray, text_size = size.small)
    table.cell(log_tbl, 1, 0, "Time",    bgcolor = color.gray, text_size = size.small)
    table.cell(log_tbl, 2, 0, "Message", bgcolor = color.gray, text_size = size.small)

    for i = 1 to log_show_msg
        arr_i = array.size(msg_arr) - log_show_msg + i - 1 - log_offset
        
        if (arr_i < 0)
            break
        
        type = array.get(type_arr, arr_i)
        
        msg_color =  type == 'message' ? #cccccc : 
                     type == 'warning' ? #F5AC4E : 
                     type == 'error'   ? #DD4224 : na
    
        table.cell(log_tbl, 0, i, str.tostring(array.get(bar_arr, arr_i)), bgcolor = msg_color, text_size = size.small)
        table.cell(log_tbl, 1, i, array.get(time_arr, arr_i),          bgcolor = msg_color, text_size = size.small)
