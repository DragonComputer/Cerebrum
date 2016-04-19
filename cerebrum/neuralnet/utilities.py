__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import rethinkdb as r # Rethinkdb Python driver

class NeuralNetUtil():

	@staticmethod
	def write_neurons(neurons, direction):
		conn = r.connect("localhost", 28015)
		r.db('test').table("neuralnet").filter({'direction': direction}).delete().run(conn)
		r.db('test').table("neuralnet").insert([
		{
			"direction": direction,
			"neurons": str(neurons)
		}
		], conflict="update").run(conn)
		conn.close()
