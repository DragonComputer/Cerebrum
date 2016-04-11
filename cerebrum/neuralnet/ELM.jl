# Types and functions
# -------------------
using DataFrames

type HiddenLayer
	# The hidden layer in ELM
	#
	# Properties
	# ----------
	# `n_hidden_neurons` is an Integer representing the total hidden neurons
	# `weight_matrix` is the input to hidden layer weight matrix which is randomly chosen
	# `bias_vector` is the randomly chosen input to hidden layer bias vector
	# `act_func` is the activation function for hidden neurons

	n_hidden_neurons::Integer
	weight_matrix::Matrix{Float64}
	bias_vector::Vector{Float64}
	act_func::Function
end

type ExtremeLearningMachine
	# Extreme Learning Machine
	#
	# Properties
	# ----------
	# `hidden_layer` is the hidden layer inside this ELM
	# `output_weights` is the weight matrix calculated during training
	# `C` is the regularisation parameter that improves generalisation (not implemented as of now)

	hidden_layer::HiddenLayer
	output_weights::Matrix{Float64}
	C::Integer

	function ExtremeLearningMachine(n_hidden_neurons::Integer;
									C = 100)
	this = new()
	this.C = C

	weight_matrix = rand(0, 0)
	bias_vector = rand(n_hidden_neurons)

	this.hidden_layer = HiddenLayer(n_hidden_neurons, weight_matrix, bias_vector, sigmoid)

	this
	end
end

function sigmoid(x)
	# Sigmoid activation

	1 ./ (1 + exp(-x))
end

function find_activations(layer::HiddenLayer,
						  x::Matrix{Float64})
	# Calculates the activations of the hidden layer neurons
	#
	# Parameters
	# ----------
	# `layer` is the HiddenLayer with neurons
	# `x` is the input matrix
	#
	# Returns
	# -------
	# Activation matrix after passing through hidden layer

	n_observations = size(x)[1]

	act_matrix = zeros(layer.n_hidden_neurons, n_observations)

	for i = 1:n_observations
	act_matrix[:, i] = layer.act_func(layer.weight_matrix * x[i, :]' + layer.bias_vector)
	end

	act_matrix
end

function fit!(elm::ExtremeLearningMachine,
			  x::Union(Matrix{Float64}, DataFrame),
			  y::Union(Vector{Float64}, DataArray{Float64, 1}, DataArray{Int64, 1}))
	# Trains the elm using the given training data
	#
	# Parameters
	# ----------
	# `elm` the ELM to train
	# `x` input data
	# `y` output data

	if typeof(x) == DataFrame
		x_mat = float(array(x))
	else
		x_mat = x
	end

	if typeof(y) != Vector{Float64}
		y_vec = float(array(y))
	else
		y_vec = y
	end


	n_observations, n_inputs = size(x_mat)
	weight_matrix = rand(elm.hidden_layer.n_hidden_neurons, n_inputs) * 2 - 1
	elm.hidden_layer.weight_matrix = weight_matrix

	act_matrix = find_activations(elm.hidden_layer, x_mat)

	output_weights = y_vec' * pinv(act_matrix)
	elm.output_weights = output_weights
end

function predict(elm::ExtremeLearningMachine,
				 x::Union(Matrix{Float64}, DataFrame))
	# Predicts the output
	#
	# Parameters
	# ----------
	# `elm` the trained ELM
	# `x` input data to predict (Matrix)

	if typeof(x) == DataFrame
		x_mat = float(array(x))
	else
		x_mat = x
	end

	act_matrix = find_activations(elm.hidden_layer, x_mat)
	vec(elm.output_weights * act_matrix)
end
