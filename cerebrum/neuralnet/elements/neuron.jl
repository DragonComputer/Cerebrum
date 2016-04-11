global neurons = []

type Neuron
	connections::Array
	potential::Int
	error::Int

	function Neuron(arg1,arg2,arg3)
		self = new(arg1,arg2,arg3)
		push!(neurons, self)
	end

end

function fully_connect(self)
	for neuron in neurons
		if object_id(neuron) != object_id(self)
			push!(self.connections, rand(1:100)/100)
		end
	end
end

function Build()
	for i = 1:10000
		Neuron([],0,0)
	end
	println(length(neurons), " neuron created.")
	n = 0
	for neuron in neurons
		n += 1
		fully_connect(neuron)
		println(n)
	end
end

Build()
