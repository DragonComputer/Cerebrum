global neurons = []

type Neuron
	dendritic_spines::Dict
	axon_terminals::Dict
	potential::Int
	create_dendritic_spines::Function

	function Neuron(arg1,arg2,arg3)
		obj = new(arg1,arg2,arg3)
		push!(neurons, obj)
	end


	function create_dendritic_spines(obj::Neuron)
		for neuron in neurons[length(obj::Neuron.dendritic_spines)]
			if object_id(neuron) != object_id(obj::Neuron)
				obj::Neuron.dendritic_spines[object_id(neuron)] = 1
			end
		end
	end

	function create_axon_terminals(obj::Neuron)
		for neuron in neurons[length(obj::Neuron.axon_terminals)]
			if object_id(neuron) != object_id(obj::Neuron)
				obj::Neuron.dendritic_spines[object_id(neuron)] = 1
			end
		end
	end

	function activate(obj::Neuron)
		while true
			sleep(2)
		end
	end
end
