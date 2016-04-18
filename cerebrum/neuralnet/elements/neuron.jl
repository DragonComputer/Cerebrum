global neurons = []

type Neuron
	connections::Dict{UInt64,Float16}
	potential::Float16
	error::Float16

	function Neuron(arg1,arg2,arg3)
		self = new(arg1,arg2,arg3)
		push!(neurons, self)
	end

end

function fully_connect(self)
	for neuron in neurons
		if object_id(neuron) != object_id(self)
			self.connections[object_id(neuron)] = rand(1:100)/100
			#push!(self.connections, rand(1:100)/100)
		end
	end
end

function partially_connect(self)
	if isempty(self.connections)
		neuron_count = length(neurons)
		#for neuron in neurons
		elected = rand(neurons,100)
		for neuron in elected
			if object_id(neuron) != object_id(self)
				#if rand(1:neuron_count/100) == 1
				self.connections[object_id(neuron)] = rand(1:100)/100
					#push!(self.connections, rand(1:100)/100)
				#end
			end
		end
		println("Neuron ID: ",object_id(self))
		println("    Potential: ",self.potential)
		println("    Error: ",self.error)
		println("    Connections: ",length(self.connections))
	end
end

function Build()
	for i = 1:1000000
		Neuron(Dict(),0.0,0.0)
	end
	println(length(neurons), " neurons created.")
	n = 0
	@parallel for neuron in neurons
		n += 1
		partially_connect(neuron)
		println("Counter: ",n)
	end
end

Build()
