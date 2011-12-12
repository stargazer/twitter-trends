from setuptools import setup, find_packages

setup(
	name = "twitter-trends",
	version = "0.1",
	packages = find_packages(),
	install_requires = [
		'setuptools',
	],
	entry_points = """
	[console_scripts]
	run = trends.kickstart:main
	""",
)
