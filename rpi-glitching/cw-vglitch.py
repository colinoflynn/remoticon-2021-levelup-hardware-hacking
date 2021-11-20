import chipwhisperer as cw
scope = cw.scope()

scope.clock.clkgen_freq = 100E6
scope.glitch.clk_src = 100E6
scope.glitch.output = "enable_only"

scope.io.glitch_hp = True

#Around 1000 causes reset, around 350-400 seemed good
scope.glitch.repeat = 350

scope.glitch.manual_trigger()