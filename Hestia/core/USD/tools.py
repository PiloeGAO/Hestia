"""
    :package:   Hestia
    :file:      tools.py
    :brief:     USD Toolset class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
from ..IO.command import run_shell_command

class USDTools():
	"""Class to create shortcut to USD Toolset.
	Source and references: https://graphics.pixar.com/usd/docs/USD-Toolset.html
	"""
	def __init__(self):
		pass

	@staticmethod
	def open_usdview(path, help=False, renderer=None, primpath=None, camera=None, mask=None, clearsettings=False, defaultsettings=False, norender=False, noplugins=False, unloaded=False, timing=False, memstats="", numThreads=0, ff=None, lf=None, cf=None, complexity="", quitAfterStartup=False, sessionLayer=None):
		"""Open USD View from USD toolset.
		For more informations, please read: https://graphics.pixar.com/usd/docs/USD-Toolset.html#USDToolset-usdview
		
		Args:
		    path (str): Path to USD scene.
		    help (bool, optional): Show help and quit.
		    renderer (str, optional): Renderer name.
		    primpath (str, optional): Path to the prim to select and frame.
		    camera (str, optional): Camera name.
		    mask (str, optional): Paths to prims to use as mask.
		    clearsettings (bool, optional): Restore default settings.
		    defaultsettings (bool, optional): Start USDView with default settings.
		    norender (bool, optional): Display only the hierarchy browser/also known as outliner.
		    noplugins (bool, optional): Start USDView without plugins.
		    unloaded (bool, optional): Start USDView without payloads loaded.
		    timing (bool, optional): Display timing stats to console.
		    memstats (str, optional): Use the Pxr MallocTags memory accounting system (usefull for debugging).
		    numThreads (int, optional): Specify the number of thread to use with USDView.
		    ff (int/float, optional): Set start frame.
		    lf (int/float, optional): Set end frame.
		    cf (int/float, optional): Set current frame.
		    complexity (str, optional): Set the complexity of the scene.
		    quitAfterStartup (bool, optional): Quit USDView after startup.
		    sessionLayer (None, optional): Stage to open with the 'sessionLayer' in place of the default anonymous.
		"""
		command = ["usdview"]

		if(help):
			command.append("--help")

		if(type(renderer) == str):
			command.append("--renderer")
			command.append(renderer)

		if(type(primpath) == str):
			command.append("--select")
			command.append(primpath)

		if(type(camera) == str):
			command.append("--camera")
			command.append(camera)

		if(type(mask) == str):
			command.append("--mask")
			command.append(mask)

		if(clearsettings):
			command.append("--clearsettings")

		if(defaultsettings):
			command.append("--defaultsettings")

		if(norender):
			command.append("--norender")

		if(noplugins):
			command.append("--noplugins")

		if(unloaded):
			command.append("--unloaded")

		if(timing):
			command.append("--timing")

		if(memstats in ["none", "stage", "stageAndImaging"]):
			command.append("--memstats")
			command.append(memstats)

		if(numThreads > 0):
			command.append("--numThreads")
			command.append(numThreads)

		if(type(ff) == float or type(ff) == int):
			command.append("--ff")
			command.append(ff)

		if(type(lf) == float or type(lf) == int):
			command.append("--lf")
			command.append(lf)

		if(type(cf) == float or type(cf) == int):
			command.append("--cf")
			command.append(cf)

		if(complexity in ["low", "medium", "high", "veryhigh"]):
			command.append("--complexity")
			command.append(complexity)

		if(quitAfterStartup):
			command.append("--quitAfterStartup")

		if(type(sessionLayer) == str):
			command.append("--sessionLayer")
			command.append(sessionLayer)

		command.append(path)

		run_shell_command(command)



	@staticmethod
	def open_usdcat(path=[], help=False, output="", usdFormat="usda", flatten=False, mask=""):
		"""Open USD cat from USD toolset.
		For more informations, please read: https://graphics.pixar.com/usd/docs/USD-Toolset.html#USDToolset-usdview
		
		Args:
		    path (str): Path to USD scene.
		    help (bool, optional): Show help and quit.
		    output (str, optional): Output path to converted file.
		    usdFormat (str, optional): Output format.
		    flatten (bool, optional): Flatten output file.
		    mask (str, optional): Paths to prims to use as mask.
		"""
		command = ["usdcat"]

		if(help):
			command.append("--help")

		if(type(output) == str and output != ""):
			command.append("--out")
			command.append(output)
		else:
			raise CoreError("USDCAT not support console output to Hestia.")

		if(usdFormat in ["usda", "usdb", "usdc"]):
			command.append("--usdFormat")
			command.append(usdFormat)

		if(flatten):
			command.append("--flatten")

		if(mask != ""):
			command.append("--mask")
			command.append(mask)
		
		if(type(path) == list):
			for i in path:
				command.append(i)
		else:
			command.append(path)

		run_shell_command(command)