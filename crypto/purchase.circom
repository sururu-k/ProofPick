pragma circom 2.1.6;
include "poseidon.circom";
include "comparators.circom";
// Fixed capacity 8. Only active orders contribute; private quantity and salt
// are tied to the buyer's registered commitment, campaign and order identifier.
template Purchase() {
    signal input context;
    signal input batch;
    signal input price;
    signal input minimum;
    signal input active[8];
    signal input tags[8];
    signal input commitments[8];
    signal input quantities[8];
    signal input salts[8];
    signal output total;
    signal output amount;
    signal output eligible;
    signal output anchor;
    component commit[8];
    component upper[8];
    component bits[8];
    component nonzero[8];
    signal running[9];
    running[0] <== 0;
    for (var i=0;i<8;i++) {
        active[i]*(active[i]-1) === 0;
        bits[i] = Num2Bits(14);
        bits[i].in <== quantities[i];
        upper[i] = LessEqThan(14);
        upper[i].in[0] <== quantities[i];
        upper[i].in[1] <== 9999;
        upper[i].out === 1;
        nonzero[i] = IsZero();
        nonzero[i].in <== quantities[i];
        nonzero[i].out === 1-active[i];
        (1-active[i])*salts[i] === 0;
        commit[i] = Poseidon(4);
        commit[i].inputs[0] <== context;
        commit[i].inputs[1] <== tags[i];
        commit[i].inputs[2] <== quantities[i];
        commit[i].inputs[3] <== salts[i];
        commit[i].out === commitments[i];
        running[i+1] <== running[i]+quantities[i];
    }
    total <== running[8];
    amount <== total*price;
    component enough = GreaterEqThan(17);
    enough.in[0] <== total;
    enough.in[1] <== minimum;
    eligible <== enough.out;
    component bindBatch = Poseidon(2);
    bindBatch.inputs[0] <== context;
    bindBatch.inputs[1] <== batch;
    anchor <== bindBatch.out;
}
component main {public [context,batch,price,minimum,active,tags,commitments]} = Purchase();
